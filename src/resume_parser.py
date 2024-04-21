from dotenv import load_dotenv
import re
import anthropic
from pdfminer.high_level import extract_text
import json


def send_to_claude_ai(client, message):
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": message}
        ]
    )

    concatenated_text = ""
    if isinstance(message.content, list):
        concatenated_text = "".join([cb.text for cb in message.content if hasattr(cb, "text")])
    return concatenated_text


# TODO: test prompting, modularity, and error handling
def parse_resume(client: anthropic.Anthropic, pdf_path: str):
    text = extract_text(pdf_path)

    template = None
    with open("src/resume_template.json", "r") as f:
        template = json.load(f)
    prompt = "Use the strict following JSON structure " + json.dumps(template) + " (no unspecified fields, filling unknowns with 'none') to structure the following resume information into the JSON format: " + text
    json_response = send_to_claude_ai(client, prompt)

    if json_response is None:
        print("Error: The response from Anthropic API is not in the expected format.")
        return None

    try:
        resume_data = json.loads(re.sub(r"^[^{]*", "", json_response).strip(" `"))

        #do not need this since we are using flask
        # with open("resume_parsed.json", "w") as f:
        #     json.dump(resume_data, f, indent=4)
        return resume_data
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        print("Problematic JSON string:", re.sub(r"^.*?{", "{", json_response).strip(" `"))
        return None


def load_resume(json_path: str):
    with open(json_path, "r") as json_file:
        return json.load(json_file)


if __name__ == "__main__":
    # init client
    load_dotenv()
    client = anthropic.Anthropic()

    pdf_path = "./resume.pdf"
    resume_json = parse_resume(client, pdf_path)

    if resume_json is not None:
        print(resume_json)
        with open("./resume_parsed.json", "w") as json_file:
            json_file.write(json.dumps(resume_json, indent=4))
    else:
        print("Failed to parse the resume.")
