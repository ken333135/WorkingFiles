# -*- coding: utf-8 -*-
"""
Interactive Dictionary
"""
import os, json
from difflib import get_close_matches

os.chdir("C:/Users/jingwenken/Desktop/Ken/AppsDev/InteractiveDict")
data = json.load(open("data.json"))

def translate(word):
    word = word.lower()
    if word in data:
        #check for number of definitions and returns each definition in a new line
        if len(data[word])==1:
            return data[word][0]
        else:
            output = ""
            for defn in data[word]:
                output = output + defn + "\n"
            return output
    elif len(get_close_matches(word,data.keys(),cutoff=0.8))==0:
        return "Sorry word does not exist!"
    else:
        #look for closest match to user input and gives suggestion
        closest_match = str(get_close_matches(word,data.keys(),cutoff=0.8)[0])
        answer = input("Did you mean %s instead? Press Y to confirm or N for No: "%closest_match)
        if answer=="Y":
            word=closest_match
            return data[word]
        elif answer=="N":
            return "Sorry word does not exist!"
        else:
            return "We did not understand your entry"
            
        
        
word = input("Please enter a word: ")
print(translate(word))

