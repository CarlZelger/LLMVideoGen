import json

import requests
import llmcloud

models=["Meta-Llama-3-8B-Instruct",
        "Awanllm-Llama-3-8B-Dolfin",
        "Awanllm-Llama-3-8B-Cumulus",
        "Mistral-7B-Instruct"]
def askLLM(q,len,model):
    url = "https://api.awanllm.com/v1/completions"

    payload = json.dumps({
    "model": models[model],
    "prompt": q,
    # "repetition_penalty": 1.1,
    # "temperature": 0.7,
    # "top_p": 0.9,
    # "top_k": 40,
    "max_tokens": len
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer 8706ae02-cbc3-412c-a057-1ec4c539615a"
    }
    failsafe = 0
    while True:
        try: 
            if failsafe == 1:
                break
            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            ret = data['choices'][0]['text']
            return ret
        except KeyError:
            print(q)
            failsafe += 1
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {"title": "Request failed"}
    
    
for i in range(4):   
    query = f"answer with only four short bullet points nothing more (no punctuation marks),  6 words max, insert a semocolon after every bulletpoint, about photosynthesis."
    print(f"{models[i]}: \n {askLLM(query,40,3)}\n")