import openai
import gpt_lib.tools as tools

openai.api_key = tools.open_file('openaiapikey.txt')