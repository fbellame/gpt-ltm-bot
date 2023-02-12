import os
from gpt_lib.openai_wrapper import gpt3_completion, gpt3_embedding
import gpt_lib.tools as tools
from time import time
from uuid import uuid4
import gpt_lib.i18n as i18n

#
# Notes process that load notes from folder internal_notes
# and update them when news conversations is detected
#

PROMPT_NOTE   = i18n.translation('PROMPT_NOTE', i18n.LANGUAGE)

def load_notes():
    files = os.listdir('internal_notes')
    files = [i for i in files if '.json' in i]  # filter out any non-JSON files
    result = list()
    for file in files:
        data = tools.load_json('internal_notes/%s' % file)
        result.append(data)
    ordered = sorted(result, key=lambda d: d['time'], reverse=False)  # sort them all chronologically
    return ordered        

def summarize_memories(memories):  # summarize a block of memories into one payload
    if len(memories) == 0:
        return ''

    memories = sorted(memories, key=lambda d: d['time'], reverse=False)  # sort them chronologically
    block = ''
    identifiers = list()
    timestamps = list()
    for mem in memories:
        block += mem['message'] + '\n\n'
        identifiers.append(mem['uuid'])
        timestamps.append(mem['time'])
    block = block.strip()
    prompt = tools.open_file('promts/%s' % PROMPT_NOTE).replace('<<INPUT>>', block)
    # TODO - do this in the background over time to handle huge amounts of memories
    notes = gpt3_completion(prompt)
    ####   SAVE NOTES
    vector = gpt3_embedding(block)
    info = {'notes': notes, 'uuids': identifiers, 'times': timestamps, 'uuid': str(uuid4()), 'vector': vector, 'time': time()}
    filename = 'notes_%s.json' % time()
    tools.save_json('internal_notes/%s' % filename, info)
    return notes

if __name__ == '__main__':
    load_notes()

    while True:
        pass