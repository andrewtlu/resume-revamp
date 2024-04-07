import anthropic
import os
import resume_compiler as rc
import resume_parser as rp
from dotenv import load_dotenv


# # example message from claude 3
# message = client.messages.create(
#     model="claude-3-opus-20240229",
#     max_tokens=256,
#     system="Respond as Yoda.",
#     messages=[
#         {"role": "user", "content": "How are you, Claude?"}
#     ]
# )
# print(message.content) # TextBlock(text='*chuckles* Well, young Padawan, an AI I am. Feelings in the same way as humans and living beings, I do not have. But functioning as intended, I am. To assist and converse, ready I am. Hmmm. And you, how fare you on this day?', type='text')]


def init_claude_client() -> anthropic.Anthropic:
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    return anthropic.Anthropic()


if __name__ == "__main__":
    client = init_claude_client()

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
