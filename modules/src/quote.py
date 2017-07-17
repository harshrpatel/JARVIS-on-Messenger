import json
from random import choice

import config
import modules
from templates.quick_replies import add_quick_reply
from templates.text import TextTemplate
import requests

def process(input, entities=None):
    output = {}
    try:
        res = requests.get('https://andruxnet-random-famous-quotes.p.mashape.com/', headers={
            'X-Mashape-Key': 'yv90xTYrT3mshRpVISKu5L3OUHLnp18eNYXjsnG4loolNcXOGY',
            "Accept": "application/json"})

        op_message = res.json()['quote'] + ' - Author \n' + res.json()['author']
        message = TextTemplate(op_message).get_message()
        message = add_quick_reply(message, 'Another one!', modules.generate_postback('quote'))
        message = add_quick_reply(message, 'Show me a fact.', modules.generate_postback('fact'))
        message = add_quick_reply(message, 'Tell me a joke.', modules.generate_postback('joke'))
        output['input'] = input
        output['output'] = message
        output['success'] = True
    except:
        output['success'] = False
    return output
