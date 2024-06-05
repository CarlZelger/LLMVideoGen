from typing import Dict, List
import requests
from pexels_api import API
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

  
def make_request(topic: str, title: str,api) -> Dict[str, str]:
    url = "https://api.llmcloud.app/v1/chat/completions"
    query = f"no additional text, I need a searchterm for a fitting Image about the topic {title}, in the context of {topic}, only respond with 3 words"

    payload = json.dumps({
        "model": "Awanllm-Llama-3-8B-Dolfin",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer 1fbabf59-8dc5-4429-9097-56a4e24b671d"
    }
    
    failsafe = 0
    
    while True:
        try: 
            if failsafe == 20:
                break
            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            ret = data['choices'][0]['message']['content']
            print(f"{title}:\n {ret} \n\n")
            # searchTerm = topic+ " " + title
            api.search(ret, page=1, results_per_page=1,)
            photos = api.get_entries()
            for photo in photos:
                response = requests.get(photo.original)
                image_path = f"image{random.randint(1, 100)}.jpeg"
                with open(image_path, "wb") as file:
                    file.write(response.content)
                # print(f"for {title} added {image_path}")
                return{title: image_path}
        except KeyError:
            failsafe += 1
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {"title": "Request failed"}
    
        
def generateImagesThreads(topic: str, titles: List[str]) -> Dict[str, str]:
    PEXELS_API_KEY = 'Po4warYDOufzQWCgu8pVZrjYLrsZgs3HAqJZW9wSIL6GqM3TO3Nz9IZ9'
    api = API(PEXELS_API_KEY)
    ret = {}
    with ThreadPoolExecutor(max_workers=len(titles)) as executor:
        futures = [executor.submit(make_request, topic, title, api) for title in titles]
        for future in as_completed(futures):
            result = future.result()
            ret.update(result)
    
    return {key: ret[key] for key in titles}

def generateImages(topic: str, titles: List[str]) -> Dict[str, str]:
    PEXELS_API_KEY = 'Po4warYDOufzQWCgu8pVZrjYLrsZgs3HAqJZW9wSIL6GqM3TO3Nz9IZ9'
    api = API(PEXELS_API_KEY)
    ret = {}
    i=0
    searchTerm = topic
    api.search(searchTerm, page=1, results_per_page=len(titles))
    photos = api.get_entries()
    for photo in photos:
        response = requests.get(photo.landscape)
        image_path = f"image{i}.jpeg"
        with open(image_path, "wb") as file:
            file.write(response.content)
        ret[titles[i]] = image_path
        i += 1
            
    # return {key: ret[key] for key in titles}
    return ret
     



