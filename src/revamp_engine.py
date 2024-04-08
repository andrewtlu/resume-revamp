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
                return rp.load_resume(json_path), False
            elif selection == 1:
                resume_path = input("Please enter the path to your resume pdf: ")
                return rp.parse_resume(client, resume_path), True
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
    # TODO: instead of dumping entire resume, approach level by level (ie, pass resume dict and focus on values that are strings and recursively tackle values that are dicts or lists)
    # if a value is a dict, do the same thing again
    # if a value is a list, print elements and ask if they are correct
    def layered_corrections(field: dict, path: list[str]=[]):
        str_fields = []
        dict_fields = []
        list_fields = []

        for key, value in field.items():
            if isinstance(value, dict):
                dict_fields.append(key)
            elif isinstance(value, list):
                list_fields.append(key)
            else:
                str_fields.append(key)
        
        # string fields
        if len(str_fields) > 0:
            print(f"String fields in {'/' + '/'.join(path)}:")
            for key in str_fields:
                print(f"\t\t{key}: {field[key]}")
            print("\tEnter the field you would like to correct and the correction with an empty string to end the input: ")
            while True:
                f = input("\t\tField: ")
                if f == '':
                    break
                c = input("\t\tCorrection: ")
                try:
                    field[f] = c
                except:
                    print("\tInvalid field. Please try again.")

            with open("tmp_resume.json", "w") as f:
                json.dump(resume, f, indent=4)

        # list fields
        if len(list_fields) == 0:
            for key in list_fields:
                if isinstance(field[key][0], dict):
                    for i, item in enumerate(field[key]):
                        layered_corrections(item, path + [key, str(i)])
                else:
                    print(f"List fields in {'/' + '/'.join(path + [key])}:")
                    for i, item in enumerate(field[key]):
                        print(f"\t\t{i}: {item}")
                    print("\tEnter the index of the item you would like to correct and the correction with an empty string to end the input: ")
                    while True:
                        i = input("\t\tIndex: ")
                        if i == '':
                            break
                        c = input("\t\tCorrection: ")
                        try:
                            field[key][int(i)] = c
                        except:
                            print("\tInvalid index. Please try again.")

            with open("tmp_resume.json", "w") as f:
                json.dump(resume, f, indent=4)

        # dict fields
        for key in dict_fields:
            layered_corrections(field[key], path + [key])

    with open("tmp_resume.json", "w") as f:
        json.dump(resume, f, indent=4)

    return layered_corrections(resume)


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
    print("Initializing Claude client...")
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
