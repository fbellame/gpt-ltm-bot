import openai
import gpt_lib.tools as tools
import gpt_lib.openai_wrapper as openai_wrapper

openai.api_key = tools.open_file('openaiapikey.txt')