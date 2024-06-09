import threading
from typing import Dict, List
from flaskr.APIs.llmcloud import *
from flaskr.APIs.pptxPython import *
from flaskr.APIs.pexels import generateImages
import time

#topic of the video
topic:str
#Pagecounter
pages:int
#titles of the different Pages
titles:List[str]
#The pagetitle acts as key and the text is the value
content:Dict[str, str]
#The pagetitle acts as key and the filepath to the image is the value
images:Dict[str, str]

def generateVideo(query: str,length: int):
    global topic, pages, titles, content, images
    start_time = time.time()
    
    def generate_text_content():
        global content
        content = generateText(query, titles)

    def generate_image_content():
        global images
        images = generateImages(query, titles)
    
    
    topic = query
    pages = length
    titles = getDataForPP(query, 4)
    
    text_thread = threading.Thread(target=generate_text_content)
    text_thread.start()
    image_thread = threading.Thread(target=generate_image_content)
    image_thread.start()

    text_thread.join()
    image_thread.join()

    pp = generatePresentation(titles, content, images)
    
    elapsed_time = time.time() - start_time
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    
    # os.startfile(pp)
    


def addQuestion():
    global titles, topic
    question = addQuestiones(titles,topic)
    pp = generatePresentation(titles, content, images,question)
    # RENDER VIDEO
    os.startfile(pp)

def getTopic():
    global topic
    return topic

    
    # flask --app flaskr --debug run  