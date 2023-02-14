import openai
import re
import os
from gpt_lib import tools
from time import sleep, time
import gpt_lib.i18n as i18n
from gpt_lib.config import Config

c = Config()

ENCODING        = i18n.translation('ENCODING', i18n.LANGUAGE)
USER            = i18n.translation('USER', i18n.LANGUAGE)
CHAT_BOT_NAME   = i18n.translation('CHAT_BOT_NAME', i18n.LANGUAGE)

COMPLETION_MODEL= c.config['MODEL']['completion_model']
EMBEDDING_MODEL = c.config['MODEL']['embedding_model']
TEMPERATURE_MODEL = float(c.config['MODEL']['model_temperature'])
MAX_TOKEN       = int(c.config['MODEL']['max_tokens'])

def gpt3_completion(prompt, engine=COMPLETION_MODEL, temp=TEMPERATURE_MODEL, top_p=1.0, tokens=MAX_TOKEN, freq_pen=0.0, pres_pen=0.0, stop=['%s:' % USER, '%s:' % CHAT_BOT_NAME]):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding=ENCODING,errors='ignore').decode(ENCODING)
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('[\r\n]+', '\n', text)
            text = re.sub('[\t ]+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            if not os.path.exists('gpt3_logs'):
                os.makedirs('gpt3_logs')
            tools.save_file('gpt3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

def gpt3_embedding(content, engine=EMBEDDING_MODEL):
    content = content.encode(encoding=ENCODING,errors='ignore').decode(ENCODING)
    response = openai.Embedding.create(input=content,engine=engine)
    vector = response['data'][0]['embedding']  # this is a normal list
    return vector  
