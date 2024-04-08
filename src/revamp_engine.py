import anthropic
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
    

def parse_resume(client: anthropic.Anthropic) -> dict:
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
    """
    while True:
        try:
            selection = select("Do you have a pre-parsed resume?", ["y", "n"])
            if selection == 0:
                json_path = input("Please enter the path to the parsed resume: ")
                return rp.load_resume(json_path)
            elif selection == 1:
                resume_path = input("Please enter the path to your resume pdf: ")
                return rp.parse_resume(client, resume_path)
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
    # for each entry:
    # print current key path (ie, education > school > classes)
    # print current value
    # prompt user to confirm or correct
    # end loop
    def correct_recursive(resume: dict|list|str, key_path: list[str]=[]) -> dict|list|str:
        if type(resume) == str:
            while True:
                print("\nField: " + " > ".join(key_path) + ":", resume)
                selection = select(f"Is the above information correct?", ["y", "n"])
                if selection == 0:
                    break
                elif selection == 1:
                    return input(f"Please enter the correct value for {' > '.join(key_path)}: ")
                else:
                    print("Invalid response. Please try again.")
        elif type(resume) == dict:
            for key, value in resume.items():
                resume[key] = correct_recursive(value, key_path + [key])
        else: # type(resume) == list
            for i, value in enumerate(resume):
                resume[i] = correct_recursive(value, key_path + [str(i)])
    
    
    return correct_recursive(resume)


if __name__ == "__main__":
    print("Initializing Claude client...")
    client = init_claude_client()
    print("Done!\n")

    resume = parse_resume(client)
    print("Resume parsed/loaded successfully.\n")

    print("Now, let's double check to ensure our copy matches yours!")
    resume = correct_resume(resume)
    messages = []

    # DONE input resume path
    # DONE parse resume, convert to json
    # double check if parsing is correct
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
