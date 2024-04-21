from flask import Flask, request, jsonify
import json
import util
import anthropic
import prompting as pr
from resume_parser import parse_resume
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024

@app.route('/')
def home():
    return None


@app.route('/initial_prompt', methods=['POST'])
def handle_initial_prompt():
    data = request.get_json()

    client = anthropic.Anthropic()  # Replace ... with your initialization parameters

    resume = data.get('resume', {})
    key = data.get('key', '')
    response = pr.initial_prompt(client, resume, key)

    # Return the response as JSON
    return jsonify({'result': response})


@app.route('/parse_resume', methods=['POST'])
def parse_resume_endpoint():
    resume_pdf = request.files.get('resume_pdf')
    if resume_pdf is None or resume_pdf.filename == '':
        return jsonify({'error': 'No file uploaded'}), 400

    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)

    pdf_path = os.path.join(uploads_dir, resume_pdf.filename)
    resume_pdf.save(pdf_path)

    client = anthropic.Anthropic()  

    parsed_resume = parse_resume(client, pdf_path)

    json_path = os.path.join(uploads_dir, 'resume_parsed.json')
    with open(json_path, 'w') as f:
        json.dump(parsed_resume, f, indent=2)

    os.remove(pdf_path)

    return jsonify({'message': 'Resume parsed successfully'}), 200



if __name__ == "__main__":
    app.run(port=5000, debug=True)
