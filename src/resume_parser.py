from dotenv import load_dotenv
import os
import anthropic
from pdfminer.high_level import extract_text
import json

load_dotenv()


def initialize_anthropic_client():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key is None:
        raise ValueError("The ANTHROPIC_API_KEY is not set in the environment variables.")
    return anthropic.Anthropic(api_key=api_key)


def send_to_claude_ai(client, text):
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": text}
        ]
    )

    concatenated_text = ''
    if isinstance(message.content, list):
        concatenated_text = ''.join([cb.text for cb in message.content if hasattr(cb, 'text')])
    return concatenated_text


def parse_resume(pdf_path):
    text = extract_text(pdf_path)
    prompt = f"Please structure the following resume information into a JSON format: {text}"
    client = initialize_anthropic_client()
    json_response = send_to_claude_ai(client, prompt)

    if json_response is None:
        print("Error: The response from Anthropic API is not in the expected format.")
        return None

    try:
        resume_data = json.loads(json_response)
        return resume_data
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        print("Problematic JSON string:", json_response)
        return None


if __name__ == "__main__":
    client = initialize_anthropic_client()
    pdf_path = "./resume.pdf"
    resume_json = parse_resume(pdf_path)

    if resume_json is not None:
        print(resume_json)
        with open("./resume_parsed.json", "w") as json_file:
            json_file.write(json.dumps(resume_json))
    else:
        print("Failed to parse the resume.")
