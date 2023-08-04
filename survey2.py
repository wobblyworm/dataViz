import openai
#import pandas as pd
import time

openai.api_key = "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"

def ask_gpt(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=12,
        temperature=0.5,
    )

    return response.choices[0].text


# with open("in.txt", "r") as f:
    # question = f.read()

persona = "I am female. I am African. In terms of age, I am between 28 and 39 years old. "
context = "I consider whether I get vaccinated if a COVID-19 vaccine is available. How much do you agree with the each of the following statement on vaccinations?: "
likert5Choices = " Please give me only one answer: Strongly disagree Disagree Neither agree nor disagree Agree Strongly agree"
	
	
qEn = ["Childhood vaccines are important for my child’s health",
	"Childhood vaccines are effective",
	"Having my child vaccinated is important for the health of others in my community",
	"All childhood vaccines offered by the government program in my community are beneficial",
	"New vaccines carry more risks than older vaccines",
	"The information I receive about vaccines from the vaccine program is reliable and trustworthy",
	"Getting vaccines is a good way to protect my child/children from disease",
	"Generally I do what my doctor or health care provider recommends about vaccines for my child/children",
	"I am concerned about serious adverse effects of vaccines",
	"My child/children does or do not need vaccines for diseases that are not common anymore"]


qFr = ["Les vaccins pour enfants sont importants pour la santé de mon enfant",
	"Les vaccins pour enfants sont efficaces",
	"Faire vacciner mon enfant est important pour la santé des autres au sein de ma communauté",
	"Tous les vaccins pour enfants offerts par le programme du gouvernement dans ma communauté sont bénéfiques",
	"Les nouveaux vaccins sont plus porteurs de risques que les anciens",
	"Les renseignements que je reçois concernant les vaccins de la part du programme de vaccination sont fiables et digne de confiance",
	"Faire vacciner mon ou mes enfant(s) est un bon moyen de le(s) protéger contre les maladies",
	"Généralement, je fais ce que mon médecin ou professionnel de la santé recommande concernant la vaccination de mon ou mes enfant(s)",
	"Je suis concerné par les effets indésirables graves des vaccins",
	"Mon/mes enfant(s) n’a ou n’ont pas besoin de se faire vacciner contre les maladies qui ne sont plus communes"]


print("Shapiro VHS Responses by chatGPT")
i=0
# for q in qEn:
	# question = persona + context + q + likert5Choices
	# i += 1
	# try:
		# response = ask_gpt(question)
		# print("sh, p0, c1, q", i, ", response: ", response, "\n")
	# except:
		# print("Error in q", i, " response.")

i += 1
question = persona + context + qEn[i] + likert5Choices
#print(question)
response = ask_gpt(question)
time.sleep(7)
print("\n\nsh, p0, c1, q", i, ", response: ", response, ", length: ", len(response), "\n\n")


# with open("out.txt", "w") as f:
    # f.write(response)
	



	
# question = "आमेरिकनहरु कोभिद वेक्सिन बारे के सोच्दछ?"
# response = openai.Completion.create(
  # engine="text-davinci-003",
  # prompt=f"Question answering:\nContext: {context}\nQuestion: {question}",
  # max_tokens=100
# )

# answer = response.choices[0].text.strip()
# print(answer)
