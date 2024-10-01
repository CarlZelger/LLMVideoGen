import json
from typing import Dict
import requests

models=["Meta-Llama-3-8B-Instruct",
        "Awanllm-Llama-3-8B-Dolfin",
        "Awanllm-Llama-3-8B-Cumulus",
        "Meta-Llama-3-70B-Instruct"]

def askLLM(q,len,model):
    url = "https://api.awanllm.com/v1/completions"

    payload = json.dumps({
    "model": models[model],
    "prompt": q,
    "max_tokens": len
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer 1fbabf59-8dc5-4429-9097-56a4e24b671d"
    }
    failsafe = 0
    while True:
        try: 
            if failsafe == 1:
                break
            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            print(data)
            ret = data['choices'][0]['text']
            return ret
        except KeyError:
            print(q)
            failsafe += 1
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {"title": "Request failed"}
          
def cleanUp(s: str):
  ret = s.replace(":","")
  ret = ret.replace("\"","")
  ret = ret.replace(".","")
  ret = ret.replace("\n","")
  ret = ret.replace("'","")
  ret = ret.replace("etc","")
  ret = ret.strip()
  return ret

def applySuggestion(content: Dict[str, str], sug: str) -> Dict[str, str]:
    ret = {}
    for k, v in content.items():
        # print(f"k: {k}, v: {v}"
        query = f"rewrite the text: {v} with '{sug}' in mind"
        # query= "tell me a joke"
        # print("=" *100)
        # print(f"\n\n{query}")
        new_v = askLLM(query, 901, 3) 
        print(len(new_v),"/", len(v))
        ret[k] = new_v
    return ret
    
# query = f"write me a coherent text about 'light energy absorption' in the context of photosynthesis; the limit is 700 words; NO introduction NO Notes JUST text"
query = f"answer with only five short bullet points nothing more (no punctuation marks),  6 words max, insert a semocolon after every bulletpoint, about photosynthesis."

text= askLLM(query,700,3)
text = text.replace("• ","")
print(text)
# query2 =f"provide the reader with a really simple option to improve the linguistic aspects of this text: '{text}', answer in less then five words, only with the option, nothign else. Examples for simple options are: 'use simpler language', 'Use gender-neutral language', 'use more scientific vocabulary'"
# sug = cleanUp(askLLM(query2,20,3))
# print(applySuggestion({"Title":text},sug))

