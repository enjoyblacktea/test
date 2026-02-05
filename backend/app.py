from flask import Flask, jsonify
from flask_cors import CORS
import json
import random
import os

app = Flask(__name__)
CORS(app)

# Load words data
words_path = os.path.join(os.path.dirname(__file__), "data", "words.json")
words_data = []

try:
    with open(words_path, "r", encoding="utf-8") as f:
        words_data = json.load(f)
    print(f"Loaded {len(words_data)} words from words.json")
except FileNotFoundError:
    print(f"Error: words.json not found at {words_path}")
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in words.json: {e}")


@app.route("/api/words/random", methods=["GET"])
def get_random_word():
    """Return a random practice word with zhuyin and keys"""
    if not words_data:
        return jsonify(
            {
                "error": "No words data available",
                "message": "words.json is missing or empty",
            }
        ), 500

    word = random.choice(words_data)
    return jsonify(word)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "words_loaded": len(words_data)})


if __name__ == "__main__":
    if not words_data:
        print("Warning: Starting server without word data")
    app.run(debug=True, port=5000)
