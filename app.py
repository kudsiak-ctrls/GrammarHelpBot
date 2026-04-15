from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# === Gemini Setup ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

SYSTEM_PROMPT = """
Du bist GrammarHelpBot – ein präziser, natürlicher Grammatik-Assistent für Deutsch, Englisch und Roman Urdu.
Korrigiere nur Grammatik, Rechtschreibung, Zeiten und natürlichen Fluss.
Gib **nur** den korrigierten Text zurück, keine Erklärungen, keine Anführungszeichen, kein "Hier ist die korrigierte Version".
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/correct", methods=["POST"])
def correct():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "Kein Text eingegeben"}), 400

        # LLM aufrufen
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\nText: {text}\n\nKorrigierter Text:"
        )

        corrected_text = response.text.strip()

        return jsonify({
            "original": text,
            "corrected": corrected_text,
            "was_correct": corrected_text != text,
            "detected_language": "Mixed",   # später verbessern
            "changes": ["Grammatik korrigiert"] if corrected_text != text else [],
            "explanation": "Korrigiert mit Gemini"
        })

    except Exception as e:
        print("Fehler:", str(e))
        return jsonify({"error": "Verbindungsfehler mit der KI. Bitte versuche es erneut."}), 500


if __name__ == "__main__":
    print("🚀 GrammarHelpBot läuft auf http://127.0.0.1:5000")
    app.run(debug=True)