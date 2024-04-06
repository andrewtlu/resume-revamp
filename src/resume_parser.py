import json
from pdfminer.high_level import extract_text
import re

def parse_resume(pdf_path):
    text = extract_text(pdf_path)
    parsed_data = {
        "education": [],
        "work_experience": [],
        "leadership_community_involvement": [],
        "additional_information": {},
    }

    education_pattern = re.compile(r"EDUCATION(.*?)WORK EXPERIENCE", re.DOTALL)
    work_experience_pattern = re.compile(r"WORK EXPERIENCE(.*?)LEADERSHIP & COMMUNITY INVOLVEMENT", re.DOTALL)
    leadership_pattern = re.compile(r"LEADERSHIP & COMMUNITY INVOLVEMENT(.*?)ADDITIONAL INFORMATION", re.DOTALL)
    additional_info_pattern = re.compile(r"ADDITIONAL INFORMATION(.*)", re.DOTALL)

    education_matches = education_pattern.search(text)
    if education_matches:
        education_content = education_matches.group(1).strip()
        parsed_data["education"] = education_content.split('\n\n')

    work_experience_matches = work_experience_pattern.search(text)
    if work_experience_matches:
        work_experience_content = work_experience_matches.group(1).strip()
        parsed_data["work_experience"] = work_experience_content.split('\n\n')

    leadership_matches = leadership_pattern.search(text)
    if leadership_matches:
        leadership_content = leadership_matches.group(1).strip()
        parsed_data["leadership_community_involvement"] = leadership_content.split('\n\n')

    additional_info_matches = additional_info_pattern.search(text)
    if additional_info_matches:
        additional_info_content = additional_info_matches.group(1).strip()
        parsed_data["additional_information"] = additional_info_content
    resume_json = json.dumps(parsed_data, indent=4, ensure_ascii=False)
    return resume_json

pdf_path = "./resume.pdf"
resume_json = parse_resume(pdf_path)

with open("./resume_parsed.json", "w", encoding="utf-8") as json_file:
    json_file.write(resume_json)

print(resume_json)
