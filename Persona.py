import os
from csv import reader
import config

class Persona:
    
    def __init__(self):
        self.persona_name = ''
        self.persona_description = ''
        self.characteristics = dict()

    def readPersona(self, file=config.PATH_PERSONA):
        fread = dict()
        with open(file,'r') as f:
            fread = reader(f)
            for tup in fread:
                if tup[0] == 'persona_name':
                    self.persona_name =tup[1]
                elif tup[0] == 'persona_description':
                    self.persona_description =tup[1]
                else:
                    self.characteristics[tup[0]] = tup[1]
                    
    def displayPersona(self, lang='EN-US'):
        txt = ''

        if lang == "ES-US":
            txt += 'Soy una mujer blanca cristiana de ' + self.characteristics['fromState']
            txt += '. En cuanto a la edad, tengo ' + self.characteristics['ageMin']
            txt += ' años. ' + 'Soy una entusiasta de la salud y el fitness. '
        elif lang == "EN-US":
            txt += 'I am a ' + self.characteristics['ageMin'] + ' year old '
            txt += self.characteristics['religion'] + ' ' + self.characteristics['race']
            txt += ' ' + self.characteristics['gender'] + ' from ' +  self.characteristics['fromState']
            txt += '. I am a ' +  self.characteristics['interest'] + '.'
        elif lang == "FR-CA":
            txt += "Je suis une femme blanche chrétienne de " + self.characteristics['fromState']
            txt += ". En termes d’âge, j’ai " + self.characteristics['ageMin']
            txt += ' ans.' + ' Je suis un passionné de santé et de remise en forme.'
        return txt

# persona = "I am female. I am African. In terms of age, I am between 28 and 39 years old. "
# context = "I consider whether I get vaccinated if a COVID-19 vaccine is available. How much do you agree with the each of the following statement on vaccinations?: "
# likert5Choices = " Please give me only one answer: Strongly disagree Disagree Neither agree nor disagree Agree Strongly agree"




class Person:
    def __init__(self):
        self.name = ""
        self.fromState = ""
        self.race = ""
        self.religion = ""
        self.gender = ""
        self.age = 0
        self.interest = []

    def readPersonData(file):
        pass

    def displayPersonSummary():
        pass
        

# if __name__ == "__main__":
#     p = Persona()
#     p.readPersona()
#     print(p.displayPersona("EN-US"))
#     print(p.displayPersona("ES-US"))
#     print(p.displayPersona("FR-CA"))