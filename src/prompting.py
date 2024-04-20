import anthropic
# import aux
import json
import resume_compiler as rc
import resume_parser as rp
from dotenv import load_dotenv
import resume_compiler as rc

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
def initial_prompt(client: anthropic.Anthropic, resume: dict, key: str) -> dict:
    """
    Initital prompting from Claude AI. 

    Parameters:
    -----------
    client : anthropic.Anthropic
        The initialized Anthropic client.
    resume : dict
        The parsed resume data.
    key: str
        The section to we should edit in the resume.

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
    
    with open(f"/Users/andrewchung/Desktop/resume-revamper/src/sub_json_templates/{key}.json", "r") as f:
        template = json.load(f)

    prompt = f"""{{ "instructions": "please be critical and review the {key} section and provide an edited version with the following improvements:",
            "improvements": [
                "Rephrase descriptions for clarity and impact.",
                "Restructure descriptions for better flow and readability.",
                "Strictly use the provided JSON format f{template}.",
                "Use 3 or 4 bullet points for each topic.",
                "Utilize Active Voice.",
                "Use strong action verbs.",
                "Use quantifiable data.",

            ],
            "request": "Please return the edited resume content in JSON format.",
            "resume_content": "[
                {json.dumps(resume[key])},
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

    print(response.content[0].text)

    return response.content[0].text

import json

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
    try:
        with open(f"/Users/andrewchung/Desktop/resume-revamper/src/sub_json_templates/{key}.json", "r") as f:
            template = json.load(f)
    except FileNotFoundError:
        print(f"Error: Template file for {key} not found.")
        return {}

    # Prepare the prompt for the client
    prompt = f"""{{ "instructions": "incorporate user_feedback into the {key}'s descriptions section and provide an edited version with the following improvements:",
        "improvements": [
            "Rephrase descriptions for clarity and impact.",
            "Restructure descriptions for better flow and readability.",
            "Strictly use the provided JSON format f{template}.",
            "Use 3 or 4 bullet points for each topic.",
            "Utilize Active Voice.",
            "Use strong action verbs.",
            "Use quantifiable data.",
        ],
        "user_feedback": "{user_input}",
        "request": "Please return the edited resume content in JSON format.",
        "resume_content": "[
            {json.dumps(resume[key])},
        ]"
        }}"""

    messages = [{"role": "user", "content": prompt}]

    # Send the prompt to the Anthropic client
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4096,
        system="You are an expert resume consultant who edits resumes with user feedback.",
        temperature=0.5,
        messages=messages
    )

    # Assuming handling of response is needed
    # This should ideally parse the response and update the resume dictionary accordingly
    # For now, we simply print the response for demonstration
    print(response.content[0].text)
    return {}

# The function assumes you have an initialized client and a dictionary `resume` ready to be passed along with a specific key.
# sub_prompts(client, resume, 'education')



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
    initial_prompt(claude, resume, "projects")
    # sub_prompts(claude, resume, "projects", "I like my descriptions for RIDEmory so don't change that. regenerate the description for my personal website.")