import anthropic
import aux
import json
import resume_compiler as rc
import resume_parser as rp
from dotenv import load_dotenv


# # example message from claude 3
# message = client.messages.create(
#     model="claude-3-sonnet-20240229",
#     max_tokens=256,
#     system="Respond as Yoda.",
#     messages=[
#         {"role": "user", "content": "How are you, Claude?"}
#     ]
# )
# print(message.content) # TextBlock(text='*chuckles* Well, young Padawan, an AI I am. Feelings in the same way as humans and living beings, I do not have. But functioning as intended, I am. To assist and converse, ready I am. Hmmm. And you, how fare you on this day?', type='text')]


def init_claude_client() -> anthropic.Anthropic:
    """
    Initializes the Anthropic client using the API key stored in the .env file.
    
    Returns:
    --------
    out: anthropic.Anthropic
        The initialized Anthropic client.
    """
    load_dotenv()
    return anthropic.Anthropic()


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
                json_path = input("Please enter the path to the parsed resume: ")
                return rp.load_resume(json_path), True
            elif selection == 1:
                resume_path = input("Please enter the path to your resume pdf: ")
                return rp.parse_resume(client, resume_path), False
            else: 
                print("Invalid response. Please try again.")
        except FileNotFoundError:
            print("File not found. Please try again.")


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


def improve_resume(client: anthropic.Anthropic, resume: dict) -> dict:
    """
    Improve the resume.

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
    # TODO: augment prompt to ask for returning json strengths/weaknesses and proposed improvements (ie, rewording, etc.)
    messages.append(create_user_message("Given the following resume in JSON format, what are some strengths and weaknesses that you see?\n" + json.dumps(resume)))

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=256,
        system="Approach the prompt as if you are a helpful hiring manager reviewing a resume.",
        messages=messages
    )

    # start cycle
    # prompt for suggestions to fix weaknesses, display to user
    # select chosen improvements and save, continue to next cycle

    pass


def compile_resume(resume: dict):
    """
    Compile the resume.

    Parameters:
    -----------
    resume : dict
        The improved resume data.
    """
    with open(input("Compiled resume json path: "), "w") as f:
        json.dump(resume, f, indent=4)

    # TODO: connect with compiler
    # rc.compile_resume(resume)


if __name__ == "__main__":
    print("Initializing Anthropic client...")
    client = init_claude_client()
    print("Done!\n")

    resume, used_json = parse_resume(client)
    print("Resume parsed/loaded successfully.\n")

    if not used_json:
        print("Now, let's double check to ensure our copy matches yours!")
        resume = correct_resume(resume)

    print("Awesome! Let's get started on improving your resume!\n")
    resume = improve_resume(client, resume)

    print("Now that youre resume is looking great, let's compile it!")
    compile_resume(resume)
    print("Resume compiled successfully! To view the compiled resume, check the path you entered. To continue improving this iteration of your resume, rerun this program and load the compiled resume json for best performance!")

    # DONE input resume path
    # DONE parse resume, convert to json
    # DONE double check if parsing is correct
    # improve resume
        # initial prompt to claude to read resume and identify weaknesses
        # display weaknesses, select which to improve
        # also prompt with other goals (rewording, etc.)
        # start cycle
            # keep track of amount of lines used to ensure similar length
            # prompt for suggestions to fix weaknesses, display to user
            # select chosen improvements and save, continue to next cycle
        # end cycle
    # ensure length of lines is satisfactory, ask if user is satisfied with end product
    # if not, prompt for more improvements and continue cycle
    # else, compile resume, save json, and display resume
