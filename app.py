from flask import Flask, request, jsonify
from bot import Bot

from datetime import datetime as dt
#how to use it:
#1) install flask by: pip install flask
#2) prpare the app:
# on linux:
# export FLASK_ENV=development
# export FLASK_APP=server.py
# on windows:
# set FLASK_ENV=development
# set FLASK_APP=app.py
#3) run the app by: flask run
#4) send POST request to url: "localhost:5000/bot/"
import logging
model = Bot()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def check_connection():
  return 'connected'

@app.route('/', methods=['POST'])
def f():
  return "SUCCESS!"

@app.route('/ans', methods=['POST'])
def ans():
  context = "Sprybot is an amazing new platform that help businesses to construct chatbot effortlessly simply by feeding the bot with description of your buisness. Sprybot was founded by group of students from BarIlan University that are enthusiastic about conversational AI. The difference between our Sprybot platform and other chat bots is that constructing traditional chat bot is a long and hard process and with Sprybot you can do it quickly and eaily. You can construct chatbot using our platform just by feeding textual description of you business that contain any details important for costumers. The time it takes to create a bot using our platform is the time takes you to describe your business. In order to create Sprybot we used natural language processing and state of the art deep learning artificial intelligence. At the moment you cant buy our product because its still under construction. Sprybot can answer questions about your business but it can not talk about anything else other than the information was fed to it."
  answer = model.ans(request.form.get('question'), context)
  response = jsonify(answer)
  response.headers.add('Access-Control-Allow-Origin', '*')
  app.logger.info(answer)
  return response

@app.route('/bot', methods=['POST'])
def bot():
  query = request.get_json()
  return jsonify(model.reply(query['context'], query['log']))
