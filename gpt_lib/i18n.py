from gpt_lib.config import Config

c = Config()

#
# Simple i18n lib to manage french and english translation (I m new to python and really don't like existing gettext)
#

LANGUAGE = c.config['GLOBAL']['language']

french = {"CHAT_BOT_NAME": "THEO", "USER": "UTILISATEUR", "ENCODING": "latin-1", "PROMPT_NOTE": "prompt_notes_fr.txt", "PROMPT_RESPONSE": "prompt_response_fr.txt"}
english = {"CHAT_BOT_NAME": "RAVEN", "USER": "USER", "ENCODING": "utf-8", "PROMPT_NOTE": "prompt_notes.txt", "PROMPT_RESPONSE": "prompt_response.txt"}

def translation(msg, lang):

    if lang == 'fr':
        return french[msg]
    elif lang == 'us':
        return english[msg]
    
    return msg