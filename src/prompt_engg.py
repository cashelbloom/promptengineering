import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import LLMChain

# from langchain.schema import BaseOutputParser

import secrets_from_secretsmanager


def get_langchain_apikey():
    try:
        with open(file_path, "r") as file:
            api_key = file.read().strip()
            if not api_key:
                raise ValueError("API key is empty")
            return api_key
    except FileNotFoundError:
        raise FileNotFoundError("The file 'langchain_apikey.txt' does not exist")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the API key: {e}")


# Construct a path relative to the current script
file_path = os.path.join(os.path.dirname(__file__), "langchain_apikey.txt")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = get_langchain_apikey()

# Get the API key from AWS Secrets Manager
api_key = secrets_from_secretsmanager.get_secret()

# # getting an instance of the ChatOpenAI class
chat_model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)
prompt_template_text = """You are a high school history teacher grading homework assignments. \
    Based on the homework question indicated by “**Q:**” and the correct answer \
    indicated by “**A:**”, your task is to determine whether the student's answer is correct. \
    Grading is binary; therefore, student answers can be correct or wrong. \
    Simple misspellings are okay.

    **Q:** {question}
    **A:** {correct_answer}

    **Student's Answer:** {student_answer}
    """

question = "Who was the first president of the United States?"
correct_answer = "George Washington"
student_answer = "George Washingon"

# prompt = ChatPromptTemplate.from_messages(
#     [AIMessage(prompt_template_text), HumanMessage(question)]
# )
prompt = [AIMessage(prompt_template_text), HumanMessage(question)]
# input_variables = (
#     [
#         {"question": question},
#         {"correct_answer": "George Washington"},
#         {"student_answer": "George Washington"},
#     ],
# )
input_variables = {
    "question": question,
    "correct_answer": "George Washington",
    "student_answer": "George Washington",
}

output = chat_model.invoke(prompt, input_variables)
# output = chat_model.invoke(prompt)
# chain = LLMChain(chat_model=chat_model, prompt=prompt)


# execute the chain
# output = chain.run(input_variables)
print(output)
