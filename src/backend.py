from flask import Flask, request, jsonify
import json
import util
import anthropic
import prompting as pr

app = Flask(__name__)

@app.route('/')

def home():
    resume = {}

    with open(util.from_base_path("src/resume_parsed.json"), "r") as f:
        resume = json.load(f)

    return jsonify(resume)

app = Flask(__name__)

@app.route('/initial_prompt', methods=['POST'])
def handle_initial_prompt():
    # Get the request data
    data = request.get_json()

    # Initialize the Anthropic client
    client = anthropic.Anthropic(...)  # Replace ... with your initialization parameters

    # Call the initial_prompt function
    resume = data.get('resume', {})
    key = data.get('key', '')
    response = pr.initial_prompt(client, resume, key)

    # Return the response as JSON
    return jsonify({'result': response})


from flask import Flask, request, jsonify
import os
import json
import anthropic
from resume_parser import parse_resume

app = Flask(__name__)

@app.route('/parse_resume', methods=['POST'])
def parse_resume_endpoint():
    # Get the resume PDF file from the request
    resume_pdf = request.files.get('resume_pdf')

    # Check if the file was uploaded properly
    if resume_pdf is None or resume_pdf.filename == '':
        return jsonify({'error': 'No file uploaded'}), 400

    # Save the uploaded PDF file temporarily
    pdf_path = os.path.join('uploads', resume_pdf.filename)
    resume_pdf.save(pdf_path)

    # Initialize the Anthropic client
    client = anthropic.Anthropic(...)  # Replace ... with your initialization parameters

    # Parse the resume PDF
    parsed_resume, _ = parse_resume(client, pdf_path)

    # Save the parsed data as a JSON file
    json_path = os.path.join('uploads', 'resume_parsed.json')
    with open(json_path, 'w') as f:
        json.dump(parsed_resume, f, indent=2)

    # Remove the temporary PDF file
    os.remove(pdf_path)

    return jsonify({'message': 'Resume parsed successfully'}), 200

# Create the uploads directory if it doesn't exist
uploads_dir = os.path.join(app.root_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == "__main__":
    app.run(port=5000, debug=True)