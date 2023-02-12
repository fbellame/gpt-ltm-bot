import os
import gpt_lib.tools as tools
from gpt_lib.openai_wrapper import gpt3_embedding, gpt3_completion
from time import time
from uuid import uuid4
import gpt_lib.i18n as i18n

#
# Nexus methods for conversation
# 
#

PROMPT_RESPONSE = i18n.translation('PROMPT_RESPONSE', i18n.LANGUAGE)
USER            = i18n.translation('USER', i18n.LANGUAGE)

def load_convo():
    files = os.listdir('nexus')
    files = [i for i in files if '.json' in i]  # filter out any non-JSON files
    result = list()
    for file in files:
        data = tools.load_json('nexus/%s' % file)
        result.append(data)
    ordered = sorted(result, key=lambda d: d['time'], reverse=False)  # sort them all chronologically
    return ordered

def save_conversation(speaker, msg, conversations):
    timestamp = time()
    vector = gpt3_embedding(msg)
    timestring = tools.timestamp_to_datetime(timestamp)
    message = '%s: %s - %s' % (speaker, timestring, msg)

    info = {'speaker': speaker, 'time': timestamp, 'vector': vector, 'message': message, 'uuid': str(uuid4()), 'timestring': timestring}
    filename = 'log_%s_%s.json' % (timestamp, speaker)
    tools.save_json('nexus/%s' % filename, info)
    conversations.append(info)

    return vector

def get_last_messages(conversation, limit):
    try:
        short = conversation[-limit:]
    except:
        short = conversation
    output = ''

    # remove last message cause it wiil be in the answer or question section from UTILISATEUR
    short = short[:-1]

    # walk through message list to make it a string
    for i in short:
        output += '%s\n\n' % i['message']
    output = output.strip()
    return output

def fetch_memories(vector, logs, count):
    scores = list()
    for i in logs:
        if vector == i['vector']:
            # skip this one because it is the same message
            continue
        score = tools.similarity(i['vector'], vector)
        i['score'] = score
        scores.append(i)
    ordered = sorted(scores, key=lambda d: d['score'], reverse=True)
    # TODO - pick more memories temporally nearby the top most relevant memories
    try:
        ordered = ordered[0:count]
        return ordered
    except:
        return ordered

def ask_theo(note, recent, user_msg):
    prompt = tools.open_file('promts/%s' % PROMPT_RESPONSE).replace('<<NOTES>>', note).replace('<<CONVERSATION>>', recent).replace('<<%s>>' % USER, user_msg)
    #### generate response, vectorize, save, etc
    output = gpt3_completion(prompt)

    return output