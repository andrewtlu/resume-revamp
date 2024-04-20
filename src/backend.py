from flask import Flask, request, jsonify
import json
import util

app = Flask(__name__)

@app.route('/')

def home():
    resume = {}

    with open(util.from_base_path("src/resume_parsed.json"), "r") as f:
        resume = json.load(f)

    return jsonify(resume)

if __name__ == "__main__":
    app.run(port=5000, debug=True)