# test_hello_add.py
from app import app
from flask import json
from datetime import datetime as dt

def build_massage(sender, datetime, text):
    return {"sender": sender, "datetime": datetime, "text": text}

def build_query(context, log):
    return {"context": context, "log": log}

def test_query():
    context = "Telegram is a messaging app with a focus on speed and security, it’s super-fast, simple and free. You can use Telegram on all your devices at the same time — your messages sync seamlessly across any number of your phones, tablets or computers. With Telegram, you can send messages, photos, videos and files of any type (doc, zip, mp3, etc), as well as create groups for up to 200,000 people or channels for broadcasting to unlimited audiences. You can write to your phone contacts and find people by their usernames. As a result, Telegram is like SMS and email combined — and can take care of all your personal or business messaging needs. In addition to this, we support end-to-end encrypted voice"
    return build_query(context=context, log=[build_massage('user', str(dt.now()), "what is Telegram?")])

def test_bot():
    query = test_query()
    response = app.test_client().post(
        '/bot',
        data=json.dumps(query),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['text'] == 'the first letter of your question is {}'.format(query['log'][-1]['text'][0])
