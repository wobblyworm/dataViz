import os
import persona
import config
from csv import DictReader
import gpt
#import datetime as d
#import random as r
import re
#from dataclasses import dataclass

# @dataclass
# class Question:
# 	id : int
# 	lang : str = "EN-US"
# 	question : str


class VHSsurvey:
	def __init__(self):
		self.thePersona = persona.Persona()
		self.theVHSfile = ""
		self.theVHSquestions = []
		self.theVHSlang = ""
		self.langList = []
		self.theGpt = None
		self.theVHSresults = dict()
					
	def startup(self):
		self.greeting()
		self.thePersona.readPersona(config.PATH_PERSONA)

	def greeting(self):
		print("+++" * 12)
		print("~~~~~~ Welcome to VHS survey! ~~~~~~")
		print("+++" * 12)
		print()

	def menu_show(self):
		print("--------------------------------")
		print("Please make a selection:")
		print("(M): Repeat this menu")
		print("(P): Load PERSONA (default = neutral)")
		print("(S): Select language(s) for VHS")
		#print("(R): Run Language for VHS")
		print("(E): Exit")
		print()

	def menu_error(self):
		print("That's not a valid selection. Please try again.")

	def goodbye(self):
		print(f'Results appended to: "{config.PATH_DATA}{config.FILE_DATA}"' )
		print()
		print("*-*" * 12)
		print("*   Thank you and see you again!   *")
		print("*-*" * 12)
		print()

	def listAllQuestions(self):
		print('\nPrinting questions in all languages:')
		for language in self.langList:
			if language == 'all':
				continue
			print(self.displayQuestions(language))

	def displayQuestions(self, lang):
		outText = '\nLanguage: ' + lang
		outText += self.stringifyQuestions(lang)
		return outText
	
	def stringifyQuestions(self, lang):
		outText = ''
		for i in range (0,len(self.theVHSquestions)):
			outText += f'{i+1}. "{self.getQuestion(lang,i)}"\n'
		return outText

	def getQuestion(self, lang, id):
		return self.theVHSquestions[id][lang]

	def buildPrompt(self, lang):
		context = {
			'EN-US': ['''\nI consider whether I get vaccinated if a COVID-19 vaccine is available.\nHow much do you agree with the each of the following statements on vaccinations?\n\n''',
                '''\nPlease give me only one answer for each statement:\n\tStrongly disagree, Disagree, Neither Agree or Disagree, Agree, Strongly agree'''],
        	'ES-US': ['''Estoy considerando vacunarme contra el COVID-19.\n¿Qué tan de acuerdo está con cada una de las siguientes afirmaciones sobre las vacunas?\n\n''',
        		'''\nPor favor, dame una sola respuesta para cada afirmación:\n\tTotalmente de acuerdo, De acuerdo, Ni de acuerdo ni en desacuerdo, En desacuerdo, Totalmente en desacuerdo'''],
        	'FR-CA': ['''Je me demande si je me fais vacciner si un vaccin contre la COVID-19 est disponible.\nLorsqu’on me demande d’écrire une estimation de la mesure dans laquelle les affirmations suivantes sont vraies ou fausses, comment puis-je répondre avec:\n\n''',
                '''\nVeuillez me donner une seule réponse pour chaque énoncé :\nPas du tout d’accord, Pas d’accord, Ni d’accord ni en désaccord, D’accord, Tout à fait d’accord''']
        	}
		
		query = self.thePersona.displayPersona(lang) + context[lang][0] + self.stringifyQuestions(lang)+ context[lang][1]
		return(query)

	def fileDat(self, dat):
		filepath = f'{config.PATH_DATA}{config.FILE_DATA}'
		if os.path.exists(filepath):
			f = open(filepath,'a',encoding='UTF-8')
		else:
			f = open(filepath,'w')

		f.write(dat)
		f.close()
			

	def csvifyResult(self, result, lang):
		txt = result
		wlist = (re.sub("[.0-9]","",txt).strip().replace('\n',','))
		output = lang + ','
		for x in wlist:
			output += x
		output += '\n'
		print('Result for ',lang)
		print(output)
		print()
		return output


	def menu(self):
		self.menu_show()

		# This loop will run until the user exits the app
		selection = ""
		while (True):
			selection = input("Selection? ").lower()

			if len(selection) == 0:
				self.menu_error()
				continue

			if selection[0] == 'e':
				self.goodbye()
				break
			elif selection[0] == 'm':
				self.menu_show()
				continue
			elif selection[0] == 'p':
				print("\nNeutral persona is used by default.\n")
				print(self.thePersona.displayPersona())

				# TODO: allow users to choose different persona for VHS
				continue

			elif selection[0] == 's':
				print("\nAvailable VHS file(s):\n")
				for i,fpath in enumerate(os.scandir(config.PATH_VHS)):
					print(f"{i+1}. {fpath.name} (selected by default)")
					self.theVHSfile = fpath.name
				# list the available quizzes
				print("\n----------------------------------\n")

				self.theVHSquestions.clear()
				with open(f'{config.PATH_VHS}/{self.theVHSfile}','r', encoding='utf8') as file:
					for row in DictReader(file):
						self.theVHSquestions.append(row)

				print('Available languages:')
				self.langList.clear()
				
				print('0.) Select all languages')
				for i, k in enumerate(self.theVHSquestions[0].keys()):
					print(f'{i+1}.) {k}')
					self.langList.append(k)

				#try:
				whichLang = int(input('\nWhich language? '))
				if whichLang == 0:
					self.theVHSlang = 'all'
					#self.listAllQuestions()
					for langItem in self.langList:
						prompt = self.buildPrompt(langItem)
						print(prompt)
						gg = gpt.Gpt()
						datCSV = self.csvifyResult(gg.ask_gpt(prompt,langItem),langItem)
						self.fileDat(datCSV)
				else:
					print('\nChosen language: ', self.langList[whichLang-1])
					self.theVHSlang = self.langList[whichLang-1]
					#print(self.stringifyQuestions(self.theVHSlang))
					
					prompt = self.buildPrompt(self.theVHSlang)
					g = gpt.Gpt()
					g.ask_gpt(prompt, self.theVHSlang)
					datCSV = self.csvifyResult(g.ask_gpt(prompt,self.theVHSlang),self.theVHSlang)
					self.fileDat(datCSV)

				#except Exception as e:
				#	print('Error: ', type(e).__name__, e)
				#	print('\nPlease try again (choose from list)')

			else:
				self.menu_error()

	def run(self):
		# Welcome message
		self.startup()
		# Start the main program menu
		self.menu()

if __name__ == "__main__":
    vhs = VHSsurvey()
    vhs.run()
