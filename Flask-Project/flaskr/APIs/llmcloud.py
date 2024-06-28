from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from typing import Dict, List
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openai import OpenAI
# from .upsplash import generateImages, genFileName


def getDataForPP(topic,pages):
    query = f"answer with only five short bullet points nothing more (no punctuation marks),  6 words max, insert a semocolon after every bulletpoint, about {topic}."
    ret = askLLM(query,30)
    print(ret)
    retList = [item.strip().lstrip('• ').lstrip('\n').capitalize() for item in ret.split(";") if item.strip()]
    return retList
    

def make_request(topic: str, title: str, url: str, headers: dict) -> Dict[str, str]:
    query = f"write me a coherent text about '{title}' in the context of {topic}; the limit is 300 words dont exeed it; NO introduction NO Notes JUST text"
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


def askLLM2(q,len):
    url = "https://api.awanllm.com/v1/completions"

    payload = json.dumps({
    "model": "Meta-Llama-3-70B-Instruct",
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
            if(response.status_code != 200):
                print(response.text)
            data = response.json()
            ret = data['choices'][0]['text']
            return ret
        except KeyError:
            print(q)
            failsafe += 1
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {"title": "Request failed"}
        
def askLLM(q,len):
    openai = OpenAI(
        api_key="eEQRbYTh5c4JGRk5YXgsK8RaEK3ge1p2",
        base_url="https://api.deepinfra.com/v1/openai",
    )

    chat_completion = openai.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        messages=[{"role": "user", "content": q}],
    )

    print(chat_completion)
    return chat_completion.choices[0].message.content

        
def verbalImprovement():
    return 0

def addTopic():
    return 0

def addQuestiones(titles: List[str],topic: str):
    i = random.randint(0,len(titles)-1)
    query = f"give me one short and simple question, without providing an answer! about the following topic: {titles[i]} in the context of {topic}; no formattion or additional text, JUST the question NO answer and NO additional Text"
    ret = askLLM(query,30)
    ret = ret.replace(".","")
    ret = ret.replace("\n","")
    ret = ret.replace(":","")
    ret = ret.replace("!","")
    return ret


def cleanUp(s: str):
    ret = s.replace(":","")
    ret = ret.replace("\"","")
    ret = ret.replace(".","")
    ret = ret.replace("\n","")
    ret = ret.replace("'","")
    ret = ret.replace("etc","")
    ret = ret.strip()
    return ret

def generateSuggestion(text:str):
    query2 =f"provide the reader with a really simple option to improve the linguistic aspects of this text: '{text}', answer in less then five words, only with the option, nothign else. Examples for simple options are: 'use simpler language', 'Use gender-neutral language', 'use more scientific vocabulary'"
    output = cleanUp(askLLM(query2,20))
    return output

def applySuggestion(content: Dict[str,str],sug: str):
    ret = {}
    for k,v in content.items():
        query = f"rewrite the text: {v} with '{sug}' in mind"
        new_v = askLLM(query,700)
        ret[k] = new_v
    return ret







