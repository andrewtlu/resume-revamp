import anthropic
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


if __name__ == "__main__":
    client = init_claude_client()
    resume = parse_resume(client)
    print(resume)
    messages = []

    # input resume path
    # parse resume, convert to json
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
