import requests
import json
from typing import List


def genFileName(input_string):
    words = input_string.split()
    words = [words[0].lower()] + [word.capitalize() for word in words[1:]]
    return ''.join(words)

# def generateImages(topic: str, titles: List[str]):
#     ret = {}
#     url = "https://api.llmcloud.app/v1/chat/completions"
#     i = 1
#     for t in titles:
#         # query =f"only 3 word description to put in a image search: {t}"
#         # payload = json.dumps({
#         #     "model": "Meta-Llama-3-8B-Instruct",
#         #     "messages": [
#         #         {
#         #             "role": "user",
#         #             "content": query
#         #         }
#         #     ]
#         # })
#         # headers = {
#         #     'Content-Type': 'application/json',
#         #     'Authorization': f"Bearer 1fbabf59-8dc5-4429-9097-56a4e24b671d"
#         # }

#         # response = requests.request("POST", url, headers=headers, data=payload)
#         # data = response.json() 
#         # print(data)
#         # imgDesc = data['choices'][0]['message']['content']
#         imgDesc = t
#         print(imgDesc)
#         # return 
#         url = f"https://api.unsplash.com/photos/random?query={imgDesc}&orientation=landscape&client_id=BXjhLvwxqzQSVTQa6hqiEjdD05vcC3Pi91FBmZ6dW9w"
#         data = requests.get(url).json()
#         img_data = requests.get(data["urls"]["regular"]).content
#         filename = genFileName(imgDesc) + ".jpg"
#         filename = f"image{i}"+ ".jpg"
#         i+= 1
#         with open(filename, "wb") as file:
#             file.write(img_data)
#             print("created file: ",filename)
#             ret[t] = filename
#     return ret
        