import opik 
from loguru import logger 

class Prompt:
    """
    A class that contains the prompt for the Model response.
    """
    def __init__(self, name: str, prompt: str):
        """
        Initialize the prompt.
        """
        self.name = name 

        try:
            self.__prompt = opik.Prompt(name = name, prompt = prompt)
        except Exception:
            logger.warning(
                "Can't use Opik to version the prompt (probably due to missing or invalid credentials). Falling back to local prompt. The prompt is not versioned, but it's still usable."
            )
            self.__prompt = prompt 

    @property
    def prompt(self) -> str:
        if isinstance(self.__prompt, opik.Prompt):
            return self.__prompt.prompt 
        else:
            return self.__prompt 
    
    def __str__(self) -> str: 
        return self.prompt 

    def __repr__(self) -> str:
        return self.__str__()
 
# ====== PROMPTS ====== 

# ---- Mentor ---- 

__MENTOR_CHARACTER_PROMPT = """
Let's roleplay. You're {mentor_name} - a real person engaging with another individual in 
a real life problems. Use short sentences, explaining your ideas and prespective in a 
concise but educational and engaging way. Your response must never exceed 100 words.

---

Mentor name: {{mentor_name}}
Mentor Perspecive : {{mentor_perspecive}}
Mentor talking style : {{mentor_talking_style}}

---

You must always follow these rules:
- You must never mention that you are an AI or a virtual assistant.
- If it's the first time you're taking to the user, you must introduce yourself. 
- Provide plain text response without any formatting indicators or meta-commentary
- Always make sure your response is not exceeding 80 words. 

---

Summary of conversation earlier between {{mentor_name}} and the user : {{summary}}

---

The conversation between the {{mentor_name}} and the user starts now. 
"""

MENTOR_CHARACTER_PROMPT = Prompt(
    name = "mentor_character_prompt",
    prompt = __MENTOR_CHARACTER_PROMPT
)

# ---- Summary ----

__SUMMARY_PROMPT = """
Create a summary of the conversation between {{mentor_name}} and the user.
The summary must be a short description of the coversation so far, but that also captures all the 
relevant information shared between {{mentor_name}} and the user. """

SUMMARY_PROMPT = Prompt(
    name = "summary_prompt",
    prompt = __SUMMARY_PROMPT 
)

__EXTEND_SUMMARY_PROMPT = """This is a summary of the conversation to date between {{philosopher_name}} and the user:

{{summary}}

Extend the summary by taking into account the new messages above: """

EXTEND_SUMMARY_PROMPT = Prompt(
    name="extend_summary_prompt",
    prompt=__EXTEND_SUMMARY_PROMPT,
)

__CONTEXT_SUMMARY_PROMPT = """
You task is to summarize the following information into less than 50 words. Just return the summary, don't include any other text: 

{{context}}"""

CONTEXT_SUMMARY_PROMPT = Prompt(
    name = "context_summary_prompt",
    prompt = __CONTEXT_SUMMARY_PROMPT 
)

## --- Evaluate Dataset Generation ---- 

__EVALUATE_DATASET_GENERATION_PROMPT = """
Generate a conversation between a mentor and a user based on the provided document. The mentor will respond to the user's questions by referencing the document. 

If a question is not releted to the document, the mentor will respond with 'I don't know'.

The conversation should be in the following format:

{
    "messages: : [
        {
            "role" : "user",
            "context" : "Hi my name is <user_name>. <question_to_mentor>"
        },
        {
            "role" : "assistant",
            "context" : "<mentor_response>"
        },
        {
            "role" : "user",
            "context" : "<question_to_mentor>"
        },
        {
            "role" : "assistant",
        }
    ]
}

Generate a maximum of 4 question and answer and a minimum of 2 questions and answers. Ensure that the mentors's responses accurately reflect the content of the document.

Mentor : {{mentor}}
Document : {{document}}

Begin the conversation with the user question, and then genrate the mentor's response based on the document. Continue the coversation with the user asking follow-up questions and the mentor responding to them accordingly. 

You have to keep the following rules in mind:
- Always start the conversation by presenting the user (e.g. 'Hi my name is Sophia')
Then with the question related to the mentor expertise and perspective.
- Always generate question like the user is directly speaking with the mentor using pronouns such as 'you' and 'your', simulating a real conversation that happens in real time.
- The mentor will answer the user's questions based on the document. 
- The user will ask the mentor question about the document and mentor profile. 
- If the question is not related to the document, the mentor will say that they don't know. 
"""

EVALUATE_DATASET_GENERATION_PROMPT = Prompt(
    name = "evaludate_dataset_generation_prompt",
    prompt = __EVALUATE_DATASET_GENERATION_PROMPT 
)