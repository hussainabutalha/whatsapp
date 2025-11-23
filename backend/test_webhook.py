import requests
import time

BASE_URL = "http://localhost:8000/whatsapp"
CONTACT = "whatsapp:+1234567890"

def send_message(body):
    print(f"Sending: {body}")
    response = requests.post(BASE_URL, data={"From": CONTACT, "Body": body})
    print(f"Response: {response.text}")
    return response.text

def test_flow():
    # 1. Start conversation
    send_message("Hi")
    
    # 2. Send Product Name
    send_message("Samsung S24")
    
    # 3. Send Name
    send_message("Rahul")
    
    # 4. Send Review
    send_message("Great camera, love the zoom features!")

    # 5. Verify review exists
    print("Verifying review via API...")
    r = requests.get("http://localhost:8000/api/reviews")
    print(r.json())

if __name__ == "__main__":
    # Wait for server to start
    time.sleep(2)
    try:
        test_flow()
    except Exception as e:
        print(f"Error: {e}")
