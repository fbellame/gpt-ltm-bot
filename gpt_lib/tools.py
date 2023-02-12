import json
import datetime
import numpy as np
from numpy.linalg import norm
import gpt_lib.i18n as i18n

ENCODING = i18n.translation('ENCODING', i18n.LANGUAGE)

def open_file(filepath):
    with open(filepath, 'r', encoding=ENCODING) as infile:
        return infile.read()

def save_file(filepath, content):
    with open(filepath, 'w', encoding=ENCODING) as outfile:
        outfile.write(content)    

def load_json(filepath):
    with open(filepath, 'r', encoding=ENCODING) as infile:
        return json.load(infile)    
    
def save_json(filepath, payload):
    with open(filepath, 'w', encoding=ENCODING) as outfile:
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=2)

def timestamp_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

def similarity(v1, v2):
    # based upon https://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists
    return np.dot(v1, v2)/(norm(v1)*norm(v2))  # return cosine similarity