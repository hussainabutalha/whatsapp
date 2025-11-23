# WhatsApp Product Review Collector

A full-stack application that collects product reviews via a WhatsApp chatbot and displays them on a React frontend.

## 🚀 Features

- **WhatsApp Integration**: Interactive chatbot flow to collect Product Name, User Name, and Review.
- **Real-time Updates**: Frontend automatically fetches and displays new reviews.
- **Backend**: Built with FastAPI and SQLAlchemy.
- **Frontend**: Built with React and Vite.
- **Database**: SQLite for easy setup (can be switched to PostgreSQL).

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite/PostgreSQL
- **Frontend**: React, Vite, Axios
- **External**: Twilio API (for WhatsApp)

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js & npm
- Twilio Account (for WhatsApp Sandbox)

### 1. Backend Setup

```bash
cd backend
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`.

### 2. Frontend Setup

```bash
cd frontend
# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### 3. Twilio Webhook Setup

To receive WhatsApp messages locally, you need to expose your backend to the internet.

1.  Install [ngrok](https://ngrok.com/).
2.  Run `ngrok http 8000`.
3.  Copy the HTTPS URL (e.g., `https://your-ngrok-url.ngrok-free.app`).
4.  Go to your [Twilio Console > Messaging > Settings > WhatsApp Sandbox Settings](https://console.twilio.com/).
5.  Paste the URL into the **When a message comes in** field, appending `/whatsapp`.
    -   Example: `https://your-ngrok-url.ngrok-free.app/whatsapp`
6.  Save settings.

## 📱 Usage

1.  Join the Twilio Sandbox by sending the code (e.g., `join <keyword>`) to the Twilio number.
2.  Send "Hi" to start the review flow.
3.  Follow the prompts to enter Product Name, Your Name, and Review.
4.  Check the React frontend to see your review appear!

## 🧪 Testing

You can run the included test script to simulate a WhatsApp webhook call:

```bash
cd backend
python test_webhook.py
```
