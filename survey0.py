import openai
import os

openai.api_key = "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"

def ask_gpt(question):
    response = openai.Completion.create(
        engine="davinci",
        prompt=question,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text

with open("question.txt", "r") as f:
    question = f.read()

response = ask_gpt(question)

with open("response.txt", "w") as f:
    f.write(response)
