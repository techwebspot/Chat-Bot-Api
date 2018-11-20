# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from urllib.parse import unquote
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from json import JSONEncoder

app = Flask(__name__)

chatbot = ChatBot(
    "Math & Time Bot",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter",
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.3,
            'default_response': 'I am sorry, but I do not understand.'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Bye',
            'output_text': 'Okay bye...'
        }
    ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    database = './database.sqlite3'
)

# Print an example of getting one math based response

conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]

chatbot.set_trainer(ListTrainer)
chatbot.train(conversation)
chatbot.set_trainer(ChatterBotCorpusTrainer)

"""
chatbot.train(
    "chatterbot.corpus.english.ai",
    "chatterbot.corpus.english.botprofile",
    "chatterbot.corpus.english.computers",
    "chatterbot.corpus.english.conversations",
    "chatterbot.corpus.english.humor",
    "chatterbot.corpus.english.gossip",
    "chatterbot.corpus.english.psychology",
    "chatterbot.corpus.english.greetings",
)
"""

@app.route('/', methods=['GET', 'POST'])
def index():
	if (request.method == 'POST'):
		some_json = request.get_json()
		return jsonify({'You sent' : some_json}), 201
	else:
		return jsonify({
			"Project" : "Chat Bot API",
			"Developed By" : "Jeet Rami"
			})

@app.route('/data/<string:message>', methods=['GET'])
def get_message(message):
	decode_message = unquote(message)
	remove_sign_message = decode_message.replace("+", " ")

	response = chatbot.get_response(remove_sign_message)

	return jsonify({'result' : str(response)})

if __name__ == '__main__':
	app.run(debug=False)