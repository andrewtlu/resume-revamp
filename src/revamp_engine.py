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
    while True:
        print(json.dumps(resume, indent=4))
        selection = select("\nIs any of the above information incorrect?", ["y", "n"])

        if selection == 0:
            print("Please enter the key paths of all the fields in the following specifications:", 
                  "\n\t1. Separate all fields via a forward slash (/),", 
                  "\n\t2. Use the dictionary key displayed above for each field and index values for lists (ie, education/0/name selects the name of the first element of the education list), and",
                  "\n\t3. Enter an empty string to finish.")
            fields = []
            while '' not in fields:
                fields.append(input(f"Key path {len(fields)}: "))
            fields.remove('')

            try:
                for field in fields:
                    path = [int(i) if i.isdigit() else i for i in field.split("/")]
                    current = resume
                    for key in path[:-1]:
                        current = current[key]
                    current[path[-1]] = input("What would you like to replace " + field + " (" + current[path[-1]] + ") with? ")

                    # store intermediate resume in case of error
                    with open("./tmp_resume.json", "w") as json_file:
                        json_file.write(json.dumps(resume, indent=4))
            except:
                print(f"Your provided keypath {field} is invalid. Please try again.")
        elif selection == 1:
            return resume
        else:
            print("Invalid response. Please try again.")


if __name__ == "__main__":
    print("Initializing Claude client...")
    client = init_claude_client()
    print("Done!\n")

    resume = parse_resume(client)
    print("Resume parsed/loaded successfully.\n")

    print("Now, let's double check to ensure our copy matches yours!\n")
    resume = correct_resume(resume)
    messages = []

    # DONE input resume path
    # DONE parse resume, convert to json
    # DONE double check if parsing is correct
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
