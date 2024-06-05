from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
# from .upsplash import generateImages, genFileName


def getDataForPP(topic,pages):
    url = "https://api.llmcloud.app/v1/chat/completions"
    query = f"answer with only the bulletpoints and the separator nothing else (no newlines or '•'), {pages} short bullet points, 6 words max, insert a semocolon after every bulletpoint, about {topic}."

    payload = json.dumps({
        "model": "Awanllm-Llama-3-8B-Cumulus",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer 8706ae02-cbc3-412c-a057-1ec4c539615a"
    }
    
    failsafe = 0
    while True:
        try: 
            if failsafe == 10:
                break
            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            ret = data['choices'][0]['message']['content']
            retList = [item.strip().lstrip('• ').lstrip('\n').capitalize() for item in ret.split(";") if item.strip()]
            return retList
        except KeyError:
            print(failsafe)
            failsafe += 1
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {"title": "Request failed"}
    

def make_request(topic: str, title: str, url: str, headers: dict) -> Dict[str, str]:
    # query = f"no additional text or formating: short focused text about {title} in the context of {topic} never more then 500 words!"
    query = f"no introduction text or formating: just talk about {title} in the context of {topic} keep it short; 600 words MAX!, less then 600 words"
    payload = json.dumps({
        "model": "Awanllm-Llama-3-8B-Cumulus",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })
    failsafe = 0
    while True:
        try:
            if failsafe == 10:
                print(f"{title}: FAILED")
                break
            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            print(len(data['choices'][0]['message']['content']))
            return {title: data['choices'][0]['message']['content']}
        except KeyError:
            print(failsafe," content")
            # print(f"{title}: hat do retry")
            failsafe += 1
        except requests.exceptions.RequestException:
            return {"title": "Request failed"}

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


    






