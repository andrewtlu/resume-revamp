import anthropic
# import aux
import json
import resume_compiler as rc
import resume_parser as rp
from dotenv import load_dotenv
import resume_compiler as rc
import re

load_dotenv()
claude = anthropic.Anthropic()



def select(prompt: str, options: list[str], case_insensitive: bool=True) -> bool:
    """
    Prompts the user with a given prompt and options, and returns a boolean value based on the user's response.

    Parameters:
    -----------
    prompt : str
        The prompt to display to the user, not including options.
    options : list[str]
        The options that the user can select from.
    case_insensitive : bool, optional
        Whether the user's response should be case-insensitive. Default is True.
    
    Returns:
    --------
    out: int
        The index of the selected option, or -1 if the user's response is invalid.
    """
    response = input(prompt + " (" + "/".join(options) + "): ")

    if case_insensitive:
        response = response.lower()
    
    try:
        return options.index(response)
    except ValueError:
        return -1 
    
def parse_resume(client: anthropic.Anthropic) -> tuple[dict, bool]:
    """
    First step in the resume revamp process. Either parses the resume using the Anthropic API and returns the parsed data or utilizes the parsed data from a JSON file.

    Parameters:
    -----------
    client : anthropic.Anthropic
        The initialized Anthropic client.
    
    Returns:
    --------
    out: dict
        The parsed resume data.
    json: bool
        Whether the resume was parsed from a JSON file or not.
    """
    while True:
        try:
            selection = select("Do you have a pre-parsed resume?", ["y", "n"])
            if selection == 0:
                json_path = '/Users/andrewchung/Desktop/resume-revamper/src/resume_parsed.json'
                return rp.load_resume(json_path), True
            elif selection == 1:
                resume_path = input("Please enter the path to your resume pdf: ")
                return rp.parse_resume(client, resume_path), False
            else: 
                print("Invalid response. Please try again.")
        except FileNotFoundError:
            print("File not found. Please try again.")



# Have API pass the section that we are working on through the API, do not move the next section until user is satisfied with the current section.
def initial_prompt(client: anthropic.Anthropic, resume: dict) -> dict:
    """
    Initital prompting from Claude AI. 

    Parameters:
    -----------
    client : anthropic.Anthropic
        The initialized Anthropic client.
    resume : dict
        The parsed resume data.

    Returns:
    --------
    out: dict
        The improved resume.
    """
    def create_user_message(content: str):
        return {"role": "user", "content": content}

    # initial prompt to claude to read resume and identify weaknesses
    # display weaknesses, select which to improve

    messages = []
    
    # dont delete this, it is easier fo rme to test isntead of deleting file path every time
    path_for_andrew = '/Users/andrewchung/Desktop/resume-revamper/src/resume_template.json'
    path = "./resume_template.json"
    with open(path_for_andrew, "r") as f:
        template = json.load(f)

    prompt = f"""{{ "instructions": "please be critical while reviewing the resume and provide an edited version with the following improvements:",
            "improvements": [
                "Rephrase descriptions for clarity and impact.",
                "Restructure descriptions for better flow and readability.",
                "Utilize Active Voice.",
                "Use strong action verbs.",s
                "Use quantifiable data.",
                "Follow the strict JSON structure in resume_content."
                "Use only specified fields.",
                "Leave Unknowns Blank.",
                "Use the JSON structure provided.",

            ],
            "request": "Please return the edited resume content in JSON format. KEEP ALL KEYS IN JSON STRUCTURE.",
            "resume_content": "[
                {json.dumps(resume)},
            ]"
            }}"""


    messages.append(create_user_message(prompt))

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4096,
        system="You are an expert resume consultant.",
        temperature=0.5,
        messages=messages
    )

    # start cycle
    # prompt for suggestions to fix weaknesses, display to user
    # select chosen improvements and save, continue to next cycle

    if isinstance(response.content, list):
        concatenated_text = "".join([cb.text for cb in response.content if hasattr(cb, "text")])

    try:
        resume_data = json.loads(re.sub(r"^[^{]*", "", concatenated_text).strip(" `"))

        #do not need this since we are using flask
        # with open("resume_parsed.json", "w") as f:
        #     json.dump(resume_data, f, indent=4)
        return resume_data
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        print("Problematic JSON string:", re.sub(r"^.*?{", "{", concatenated_text).strip(" `"))
        return None






def sub_prompts(client: anthropic.Anthropic, resume: dict, key: str, user_input: str) -> dict:
    """
    Refine the details of the outcomes that were given by the Claude Output.

    Parameters:
    -----------
    client : anthropic.Anthropic
        The initialized Anthropic client.
    resume : dict
        The parsed resume data.
    key: str
        The section of the resume that should be edited.

    Returns:
    --------
    out: dict
        The improved resume.
    """
    # Load the JSON template for the specified section
    path_for_andrew = f'/Users/andrewchung/Desktop/resume-revamper/src/sub_json_templates/{key}.json'
    try:
        with open(path_for_andrew, "r") as f:
            template = json.load(f)
    except FileNotFoundError:
        print(f"Error: Template file for {key} not found.")
        return {}

    # Initial prompt chain 1 : check for all positional argument queries given by user.
    if  key == 'projects' or key == 'experience' or  key == "other":
        prompt_initial = f"""{{ instructions": "Strictly use JSON structure outlined in the {key} key and do not add more keys. Follow the user_input for text editing operations in the {key} section.t":",
                        "{key}": {json.dumps(resume)},     
                        }}"""
    else:
        prompt_initial = f"""{{ instructions": "Strictly use JSON structure outlined in the {key} key and do not add more keys. Follow the user_input for text editing operations in the {key} section.t":",
                        "user_input": "{user_input}",
                        "{key}": {json.dumps(resume)},     
                        }}"""

    messages = [{"role": "user", "content": prompt_initial}]

    response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=4096,
    system="You are an expert at following user editing commands.",
    temperature=0.5,
    messages=messages
    )

    if isinstance(response.content, list):
        concatenated_text = "".join([cb.text for cb in response.content if hasattr(cb, "text")])
        section_data = json.loads(re.sub(r"^[^{]*", "", concatenated_text).strip(" `"))
        print(section_data)

    #prompt chain 2: enhance the resume content
    if key == "education" or key == "header" or key == "other":
        return section_data
    else:
        prompt = f""""{{instructions": "Strictly follow the JSON structure outlined in the {key} key. You must utilize user_feedback into the {key} section in resume_content with the following improvements:",
            "user_feedback": {user_input},  
            "improvements": [   
                "Please keep the number of values given for each section.",
                "Change descriptions for better flow and readability if requested.",
                "Leave Unknowns Blank.",
                "Utilize Active Voice.",
                "Use strong action verbs.",
            ],
            "request": "Please return the edited resume content in JSON format and only use keys defined in {key} key.",
            "{key}": {json.dumps(section_data)} 
        }}"""

    messages = [{"role": "user", "content": prompt}]


    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4096,
        system="You are an expert at following user editing commands.",
        temperature=0.5,
        messages=messages
    )

    print(response.content)

    if isinstance(response.content, list):
        concatenated_text = "".join([cb.text for cb in response.content if hasattr(cb, "text")])

    try:
        resume_data = json.loads(re.sub(r"^[^{]*", "", concatenated_text).strip(" `"))
        return resume_data
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        print("Problematic JSON string:", re.sub(r"^.*?{", "{", concatenated_text).strip(" `"))
        return None



def correct_resume(resume: dict) -> dict:
    """
    Double check parsed resume with user to ensure correctness.

    Parameters:
    -----------
    resume : dict
        The parsed resume data.
    
    Returns:
    --------
    out: dict
        The user-corrected resume data.
    """
    def correct_section(section, path: list[str]):
        if isinstance(section, str):
            print(f"/{'/'.join(path)}:".ljust(35) + section)
            response = input(f"\t-> ")
            if response != "":
                return response
        elif isinstance(section, list):
            for i, item in enumerate(section):
                section[i] = correct_section(item, path + [str(i)])
        else:
            for key, value in section.items():
                section[key] = correct_section(value, path + [key])
        

    print("If no corrections need to be made, just hit enter to move on.")
    for key, value in resume.items():
        resume[key] = correct_section(value, [key])



if __name__ == "__main__":

    resume, used_json = parse_resume(claude)
    print("Resume parsed/loaded successfully.\n")

    if not used_json:
        print("Now, let's double check to ensure our copy matches yours!")
        resume = correct_resume(resume)

    print("Awesome! Let's get started on improving your resume!\n")
    # print(resume)
    initial_prompt(claude, resume)
    # sub_prompts(claude, resume, "projects", "I like my descriptions for RIDEmory so don't change that. regenerate the description for my personal website.")