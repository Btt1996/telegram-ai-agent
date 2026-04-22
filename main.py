import os
from flask import Flask, request
from telegram import Bot
from fpdf import FPDF

# ------------------ CONFIG ------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Missing TOKEN environment variable")

bot = Bot(token=TOKEN)
app = Flask(__name__)


# ------------------ PDF TOOL ------------------
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    filename = "report.pdf"
    pdf.output(filename)
    return filename


# ------------------ SIMPLE AGENT LOGIC ------------------
def agent_logic(user_input):
    return f"""
REPORT: {user_input}

1. Introduction
This report is about {user_input}.

2. Key Points
- Overview of the topic
- Main applications
- Key insights

3. Conclusion
Summary of {user_input}.
"""


# ------------------ TELEGRAM WEBHOOK ------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if "message" not in data:
        return "no message", 200

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if not text:
        return "no text", 200

    # Agent step
    result = agent_logic(text)

    # PDF generation
    pdf_file = create_pdf(result)

    # Send file back
    with open(pdf_file, "rb") as f:
        bot.send_document(chat_id=chat_id, document=f)

    return "ok", 200


# ------------------ HEALTH CHECK ------------------
@app.route("/")
def home():
    return "Telegram AI Agent is running", 200


# ------------------ RUN (FOR LOCAL ONLY) ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
