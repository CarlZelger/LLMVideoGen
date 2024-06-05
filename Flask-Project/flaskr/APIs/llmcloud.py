from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
# from .upsplash import generateImages, genFileName


def getDataForPP(topic,pages):
    # query = f"answer with only the bulletpoints and the separator nothing else (no newlines or '•'), four short bullet points not more, 6 words max, insert a semocolon after every bulletpoint, about {topic}."
    # query = f"only 4 short bullepoints about {topic};5 words max; no formating(no - or numeration) or additional text; insert a semicolon after every bulletpoint."
    # query = f"NO fromatig or introduction; give me 4 short bulletpoints about {topic} no longer then 4 words each; separate them with semicolons"
    query = f"answer with only four short bullet points nothing more (no punctuation marks),  6 words max, insert a semocolon after every bulletpoint, about {topic}."
    ret = askLLM(query,30)
    retList = [item.strip().lstrip('• ').lstrip('\n').capitalize() for item in ret.split(";") if item.strip()]
    return retList
    

def make_request(topic: str, title: str, url: str, headers: dict) -> Dict[str, str]:
    # query = f"no additional text or formating: short focused text about {title} in the context of {topic} never more then 500 words!"
    # query = f"no introduction text or formating: just talk about {title} in the context of {topic} keep it short; 600 words MAX!, less then 600 words"
    query = f"write me a coherent text about '{title}'; the limit is 700 words; NO introduction NO Notes JUST text"
    print(query)
    content = askLLM(query,700)
    return {title: content}

def generateText(topic: str, titles: List[str]) -> Dict[str, str]:
    url = "https://api.llmcloud.app/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 8706ae02-cbc3-412c-a057-1ec4c539615a'
    }

    ret = {}
    with ThreadPoolExecutor(max_workers=len(titles)) as executor:
        futures = [executor.submit(make_request, topic, title, url, headers) for title in titles]
        for future in as_completed(futures):
            result = future.result()
            ret.update(result)
    
    return {key: ret[key] for key in titles}


def askLLM(q,len):
    url = "https://api.awanllm.com/v1/completions"

    payload = json.dumps({
    "model": "Mistral-7B-Instruct",
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

    
# print(askLLM("explain engines"))





