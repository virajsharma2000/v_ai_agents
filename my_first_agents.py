import requests
import json
import playsound
import glob

def execute_agent(user_prompt, tools):
  api_key = "YOUR_GEMINI_API_KEY"

  system_prompt = f'the tools given here {tools}, tell me which tool to call for the prompt given below\n{user_prompt} if the tool in not in the json of tool, return the answer of the prompt given above, if the prompt is not relavent to the tools, answer the prompt given above, else return "call_tool-tool_name+inputs-inputs_to_be_passed_in_the_tool(each input to be seperated by comma and if the input should not passed, just write "None")" without giving extra info just give the tool name without describing the reason to opt the tool and return the answer just in 1 line and the answer of the above prompt if the tool name is None'

  myobj = {"contents":[{"parts":[{"text":system_prompt}]}]}

  response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}", json = myobj)
  ai_response = response.json()['candidates'][0]['content']['parts'][0]['text']
   
  tool_name = ai_response.split('+')[0]

  if tool_name.split('-')[0] == 'call_tool':
   for tool in tools:
    if tool_name.split('-')[1].strip() == tool['tool_name']:
     tool_function = tool['tool_function']
     
     inputs_to_be_passed = ai_response.split('+')[1].split('-')[1].strip()

     if inputs_to_be_passed != 'None':
      data = tool_function(*inputs_to_be_passed.split(','))

     else:
      data = tool_function()

     if data is not None:
      try:
       data = json.loads(data)

       system_prompt = f'using the data {data}, {user_prompt}'
 
       myobj = {"contents":[{"parts":[{"text":system_prompt}]}]}

       response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}", json = myobj)
       prompt_response = response.json()['candidates'][0]['content']['parts'][0]['text']

       return prompt_response
     
      except ValueError:
       break

  else:
    return ai_response


def play_bhajan(bhajan_name):
 bhajans_and_files = {
  'powerfull hanuman chalisa':'/home/viraj/Downloads/Powerful Hanuman Chalisa.mp3',
  'ye chamak ye damak':'/home/viraj/Downloads/Ye-Chamak-Ye-Damak-2.mp3'
 }
 
 playsound.playsound(bhajans_and_files.get(bhajan_name))

def get_pc_files():
 files = glob.glob('*.*')
 files_and_names = []

 for file in files:
  files_and_names.append({'file_name':file})

 return json.dumps(files_and_names)

  
tools = [
 {'tool_name':'play bhajan', 'tool_description':'plays beautiful hindu bhajans', 'tool_function':play_bhajan},
 {'tool_name':'get pc files', 'tool_description':'gets the files stored in pc', 'tool_function':get_pc_files},
]

prompt = input('Enter prompt: ')

ans = execute_agent(prompt, tools)

if ans is not None:
 print(ans)  


