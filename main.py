import os
from flask import Flask, request
from telegram import Bot
from fpdf import FPDF

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

# ---------- PDF TOOL ----------
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    filename = "report.pdf"
    pdf.output(filename)
    return filename


# ---------- SIMPLE AGENT ----------
def agent_logic(user_input):

    return f"""
REPORT ON: {user_input}

1. Introduction
This document explains {user_input}.

2. Key Points
- Overview of the topic
- Real-world applications
- Important insights

3. Conclusion
Summary of {user_input}.
"""


# ---------- TELEGRAM WEBHOOK ----------
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    result = agent_logic(text)
    pdf = create_pdf(result)

    bot.send_document(chat_id, open(pdf, "rb"))

    return "ok"


@app.route("/")
def home():
    return "AI Agent Running"
