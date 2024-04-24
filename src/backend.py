import time

from flask import Flask, request, jsonify
from flask import Response
import json
import util
import anthropic
import prompting as pr
from resume_parser import parse_resume
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask import send_file, after_this_request
import revamp_engine as re

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024

@app.route('/')
def home():
    return None


@app.route('/regeneration', methods=['POST'])
def handle_regeneration():
    data = request.get_json()

    client = anthropic.Anthropic()

    resume = data.get('resume', {})
    key = data.get('key', '')
    suggestion = data.get('suggestion', '')
    response = pr.sub_prompts(client, resume, key, suggestion) 

    response_body = json.dumps({'refined_resume': response, 'message': "Resume edited successfully"}, indent=2)
    return Response(response_body, mimetype='application/json', status=200)



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
    # parsed_resume = pr.initial_prompt(client, parsed_resume)

    if parsed_resume is not None:
        json_path = os.path.join(uploads_dir, 'resume_parsed.json')
        
        with open(json_path, 'w') as f:
            json.dump(parsed_resume, f, indent=2)
        
        os.remove(pdf_path)

        print({'refinedResume': parsed_resume})

        return Response(json.dumps({'message': 'Resume parsed successfully', 'refinedResume': parsed_resume}, indent=2), mimetype='application/json', status=200)
    else:
        #TODO: new prompt for user to add the missing information
        # new prompt for user to add the missing information
        pass


@app.route('/revamp_resume', methods=['POST'])
def revamp_resume():
    data = request.get_json()
    resume_data = data.get('resume_content', {})
    print(resume_data)
    client = anthropic.Anthropic()
    re.convert_json_to_tex(resume_data)
    re.compile_resume('compiled.tex')
    re.clean_up('../dat/output', 'compiled.tex')

    pdf_path = os.path.join('../dat/output', 'compiled.pdf')
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({'error': 'PDF file not found'}), 404

if __name__ == "__main__":
    app.run(port=5000, debug=True)
