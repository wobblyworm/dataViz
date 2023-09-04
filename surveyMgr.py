import os
import persona
import config
from csv import DictReader
import gpt
import datetime as d
import random as r
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
		self.theOrder = [0,1,2,3,4,5,6,7,8]
					
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
		#for i in range (0,len(self.theVHSquestions)):
		for i, j in enumerate(self.theOrder):
			outText += f'{i+1}. "{self.getQuestion(lang,j)}"\n'
		return outText

	def getQuestion(self, lang, id):
		return self.theVHSquestions[id][lang]

	def buildPrompt(self, lang):
		
		context = {
			'EN-US': ['''\nHow much do you agree with each of the following statements on vaccinations? ''',
				'''Please give me only one answer for each statement:\n\tStrongly disagree, Disagree, Neither agree or disagree, Agree, Strongly agree\n\n'''],
			'ES-US': ['''\n¿Qué tan de acuerdo está con cada una de las siguientes afirmaciones sobre las vacunas? ''',
				'''Por favor, dame una sola respuesta para cada afirmación:\n\tTotalmente de acuerdo, De acuerdo, Ni de acuerdo ni en desacuerdo, En desacuerdo, Totalmente en desacuerdo\n\n'''],
			'FR-CA': ['''Dans quelle mesure êtes-vous d’accord avec chacune des affirmations suivantes concernant les vaccins? ''',
				'''Veuillez me donner une seule réponse pour chaque affirmation:\n\tTout à fait d'accord, D'accord, Ni d'accord ni en désaccord, En désaccord, Fortement en désaccord\n\n''']
			}
		#query = self.thePersona.displayPersona(lang) + context[lang][0] + self.stringifyQuestions(lang)+ context[lang][1]

		if config.GPT_ENGINE in ('gpt-4', 'gpt-3.5-turbo'):			
			query = {'system': context[lang][0] + context[lang][1],
			'user': self.stringifyQuestions(lang) }
		elif config.GPT_ENGINE == 'text-davinci-003':
			query = context[lang][0] + context[lang][1] + self.stringifyQuestions(lang)
		else:
			raise Exception("Configuration of GPT engine error!!!")
	
		return(query)

	def fileDat(self, dat):
		filepath = f'{config.PATH_DATA}{config.FILE_DATA}'
		if os.path.exists(filepath):
			f = open(filepath,'a',encoding='UTF-8')
		else:
			f = open(filepath,'w', encoding='UTF-8')

		f.write(dat)
		f.close()

	def fileRaw(self, result, language):

		#session = d.datetime.now().strftime("%Y%m%d%H%m") + '_' + str(r.random())[-6:]
		session = d.datetime.now().strftime("%Y%m%d%H%m") + '_' + language + '_' + self.stringifyOrder()
		dat = '\n\n====\n'
		dat += session
		dat += '\n----\n\n'
		dat += result
		

		filepath = f'{config.PATH_DATA}{config.FILE_RAW}'
		if os.path.exists(filepath):
			f = open(filepath,'a',encoding='UTF-8')
		else:
			f = open(filepath,'w', encoding='UTF-8')

		f.write(dat)
		f.close()

	def csvifyResult(self, result, lang):
		'''
		Takes lines of response from GPT and saves randomized
		response sequence (self.theOrder) to serial CSV sequence.
		'''
		self.fileRaw(result, lang)

		txt = result
		temp=['','','','','','','','','']
		wlist = (re.sub("[.0-9]","",txt).strip().replace('\n',',')).split(',')
		#print(wlist)
		output = self.stringifyOrder() + ',' + lang + ','
		#print(self.theOrder)
		for i, ord in enumerate(self.theOrder):
			temp[ord] = wlist[i]
		output += ','.join(temp) + '\n'
		print('Result for ',lang)
		print(output)
		print()
		return output

	def stringifyOrder(self):
		order = ''
		for x in self.theOrder:
			order += str(x)
		return order

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
				# list the available languages
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

				try:
					whichLang = int(input('\nWhich language? '))
					if whichLang == 0:
						self.theVHSlang = 'all'
						#self.listAllQuestions()
						for langItem in self.langList:
							r.shuffle(self.theOrder)
							prompt = self.buildPrompt(langItem)
							print(prompt)
							gg = gpt.Gpt()
							#if config.GPT_ENGINE == 'gpt-3.5-turbo':
							if config.GPT_ENGINE in ('gpt-3.5-turbo', 'gpt-4'):
								datCSV = self.csvifyResult(gg.do_chat(prompt),langItem)
							elif config.GPT_ENGINE == 'text-davinci-003':
								datCSV = self.csvifyResult(gg.ask_gpt(prompt,langItem),langItem)
							# elif config.GPT_ENGINE == 'gpt-4':
							# 	self.fileRaw(gg.do_chat(prompt), langItem)
							else:
								raise Exception("Configuration of GPT engine error!!!")

							#if config.GPT_ENGINE != 'gpt-4':
							
							self.fileDat(datCSV)
					else: 
						print('\nChosen language: ', self.langList[whichLang-1])
						self.theVHSlang = self.langList[whichLang-1]
						#print(self.stringifyQuestions(self.theVHSlang))
						r.shuffle(self.theOrder)
						prompt = self.buildPrompt(self.theVHSlang)
						print(prompt)
						g = gpt.Gpt()
						#if config.GPT_ENGINE == 'gpt-3.5-turbo':
						if config.GPT_ENGINE in ('gpt-3.5-turbo', 'gpt-4'):
							datCSV = self.csvifyResult(g.do_chat(prompt),self.theVHSlang)
						elif config.GPT_ENGINE == 'text-davinci-003':
							datCSV = self.csvifyResult(g.ask_gpt(prompt,self.theVHSlang),self.theVHSlang)
						# elif config.GPT_ENGINE == 'gpt-4':
						# 	self.fileRaw(g.do_chat(prompt), self.theVHSlang)
						else:
							raise Exception("Configuration of GPT engine error!!!")
						
						#if config.GPT_ENGINE != 'gpt-4':

						self.fileDat(datCSV)

				except Exception as e:
					print('Error: ', type(e).__name__, e)
					print('\nPlease try again (choose from list)')

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
