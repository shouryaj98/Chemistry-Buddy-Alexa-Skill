import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import sqlite3
import json

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():
    welcome_msg = "What's your question?"
    return question(welcome_msg)

@ask.intent("AskFormula", convert={'name': str})
def ask_formula(name):

    print("What is formula of ."+name+".")
    conn = sqlite3.connect('chem_db2')
    answer = None
    cursor = conn.execute("SELECT column2 from chem where column1 like '"+name.strip().lower()+"'")
    for row in cursor:
        answer = row[0]
    conn.close()
    if answer != None:
        answer = "the formula is "+" ".join(answer)+"."
    else:
        answer = "i dont know that one."
    answer+=" do you have any other question?"
    return question(answer)
    

@ask.intent("AskName", convert={'formula': str})
def ask_name(formula):
    print("What is name of ."+formula+".")
    conn = sqlite3.connect('chem_db2')
    answer=None
    cursor = conn.execute("SELECT column1 from chem where column2='"+formula.strip().lower().replace(".","")+"'")
    for row in cursor:
        answer = row[0]
    conn.close()
    if answer != None:
        answer = "the name is "+answer+"."
    else:
        answer = "i dont know that one."
    answer+=" do you have any other question?"
    return question(answer)


@ask.intent("YesIntent")
def yes():
    welcome_msg = "What's your question?"
    return question(welcome_msg)

@ask.intent("AMAZON.FallbackIntent")
def fallback():
    return question("I am not sure what you mean.") 

@ask.intent("AMAZON.StopIntent")
def stop():
    print("Stop")
    return statement("Okay. Goodbye") 

@ask.intent("AMAZON.CancelIntent")
def cancel():
    print("Cancel")
    return statement("Okay. Goodbye") 

@ask.intent("AMAZON.HelpIntent")
def help():
    msg = "Hi I am your Chemistry Buddy. Ask me the name or formula of any chemical compound and I will reply with the corresponding answer. Come on, what are you waiting for ? Shoot questions."
    return question(msg) 

if __name__ == '__main__':
    app.run(debug=True)
