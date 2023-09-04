import openai
import datetime as d
import random as r
import os
import config
from persona import Persona


class Gpt:

    def __init__(self):
        openai.api_key = config.API_KEY2
        #self.session = d.datetime.now().strftime("%Y%m%d%H%m") + '_' + str(r.random())[-6:]
        self.theLang = ''
    
    def getMaxTokens(self, language):
        if config.ASK_ONEONLY:
            tokens = {'EN-US': 9, 'ES-US': 15, 'FR-CA': 17}
        else:
            tokens = {'EN-US': 75, 'ES-US': 120, 'FR-CA': 140}

        return tokens[language]

    def ask_gpt(self, thePrompt, lang):
        self.theLang = lang
        outText = ''
        if config.GPT_ENGINE in ('gpt-4', 'gpt-3.5-turbo'):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": thePrompt['cmd']},
                    {"role": "user", "content": thePrompt['ques']}
                    ],
                max_tokens=self.getMaxTokens(lang),
                temperature=0.5,
            )
            outText = response['choices'][0]['message']['content']

        elif config.GPT_ENGINE in ('text-davinci-003'):
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=thePrompt,
                max_tokens=self.getMaxTokens(lang),
                temperature=0.5,
            )
            outText = response.choices[0].text
        else:
            raise Exception('config.GPT_ENGINE issues from gpt.py')
        return outText



# if __name__ == "__main__":

#     lang = 'FR-CA'
#     p = Persona()
#     p.readPersona()
#     #print(p.displayPersona('EN-US'))
    
#     g = Gpt()
#     print(query)
#     print(getResult())
#     print(g.ask_gpt(query))