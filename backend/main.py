from fastapi import FastAPI, Depends, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from twilio.twiml.messaging_response import MessagingResponse

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reviews", response_model=List[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).offset(skip).limit(limit).all()
    return reviews

@app.post("/whatsapp")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...), db: Session = Depends(get_db)):
    # Twilio sends 'From' as 'whatsapp:+1234567890'
    contact_number = From.replace("whatsapp:", "")
    message_body = Body.strip()
    
    # Get current state
    state_record = db.query(models.ConversationState).filter(models.ConversationState.contact_number == contact_number).first()
    
    resp = MessagingResponse()
    
    if not state_record:
        # New conversation
        state_record = models.ConversationState(contact_number=contact_number, state="INIT", temp_data={})
        db.add(state_record)
        db.commit()
        db.refresh(state_record)
        
        resp.message("Which product is this review for?")
        state_record.state = "ASKED_PRODUCT"
        db.commit()
        return Response(content=str(resp), media_type="application/xml")

    if state_record.state == "ASKED_PRODUCT":
        state_record.temp_data = {"product_name": message_body}
        state_record.state = "ASKED_NAME"
        db.commit()
        resp.message("What's your name?")
        return Response(content=str(resp), media_type="application/xml")

    if state_record.state == "ASKED_NAME":
        current_data = dict(state_record.temp_data)
        current_data["user_name"] = message_body
        state_record.temp_data = current_data
        state_record.state = "ASKED_REVIEW"
        db.commit()
        product_name = current_data.get("product_name")
        resp.message(f"Please send your review for {product_name}.")
        return Response(content=str(resp), media_type="application/xml")

    if state_record.state == "ASKED_REVIEW":
        current_data = dict(state_record.temp_data)
        product_name = current_data.get("product_name")
        user_name = current_data.get("user_name")
        
        # Save review
        new_review = models.Review(
            contact_number=contact_number,
            user_name=user_name,
            product_name=product_name,
            product_review=message_body
        )
        db.add(new_review)
        
        # Reset state
        db.delete(state_record)
        db.commit()
        
        resp.message(f"Thanks {user_name} -- your review for {product_name} has been recorded.")
        return Response(content=str(resp), media_type="application/xml")

    # Fallback
    resp.message("Type 'Hi' to start a new review.")
    # Reset state if stuck? Or just leave it.
    # For now, let's just reset if they say Hi
    if message_body.lower() == "hi":
         db.delete(state_record)
         db.commit()
         # Recursive call or just ask again? Let's just ask again
         new_state = models.ConversationState(contact_number=contact_number, state="ASKED_PRODUCT", temp_data={})
         db.add(new_state)
         db.commit()
         resp = MessagingResponse()
         resp.message("Which product is this review for?")
         
    return Response(content=str(resp), media_type="application/xml")

from fastapi import Response
