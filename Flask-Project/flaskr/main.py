import threading
from typing import Dict, List
from flaskr.APIs.llmcloud import *
from flaskr.APIs.pptxPython import *
from flaskr.APIs.elaiio import *
from flaskr.APIs.pexels import generateImages
import time

#topic of the video
topic:str = "tmp"
#Pagecounter
pages:int
#titles of the different Pages
titles:List[str] = ["tmp1","tmp2"]
#The pagetitle acts as key and the text is the value
content:Dict[str, str]
#The pagetitle acts as key and the filepath to the image is the value
images:Dict[str, str]

optionalTitle:str = "tmp"
suggestion:str = "tmp"

def generateVideo(query: str,length: int):
    global topic, pages, titles, content, images, optionalTitle,suggestion
    
    def generate_text_content():
        global content
        content = generateText(query, titles)

    def generate_image_content():
        global images
        images = generateImages(query, titles)
        
    topic = query
    pages = length
    titles = getDataForPP(query, 5)
    optionalTitle = titles.pop()
    optionalTitle = optionalTitle.replace(".","")
    
    text_thread = threading.Thread(target=generate_text_content)
    text_thread.start()
    image_thread = threading.Thread(target=generate_image_content)
    image_thread.start()

    text_thread.join()
    image_thread.join()
    
    text = random.choice(list(content.values()))
    suggestion = generateSuggestion(text)

    pp = generatePresentation(titles, content, images)
    # ret = render(pp)
    # if ret != "error":
    # os.startfile(ret)
        
    


def addQuestion():
    global titles, topic
    question = addQuestiones(titles,topic)
    pp = generatePresentation(titles, content, images,question)
    # RENDER VIDEO
    os.startfile(pp)
    
def addTitleToVideo():
    global titles, topic
    titles.append(optionalTitle)
    def generate_text_content():
        global content
        additionalContent = generateText(topic, [optionalTitle])
        content.update(additionalContent)

    def generate_image_content():
        global images
        images = generateImages(topic, titles)
        
    text_thread = threading.Thread(target=generate_text_content)
    text_thread.start()
    image_thread = threading.Thread(target=generate_image_content)
    image_thread.start()
    
    text_thread.join()
    image_thread.join()

    pp = generatePresentation(titles, content, images)
        
    # RENDER VIDEO
    os.startfile(pp)
    
def applySuggestion():
    global titles, content, images, suggestion
    
    content = applySuggestion(content,suggestion)
    text = random.choice(list(content.values()))
    suggestion = generateSuggestion(text)
    pp = generatePresentation(titles, content, images)
        
    # RENDER VIDEO
    os.startfile(pp)

def applyUInput(title:str, input:str):
    global titles, content, images
    newContent = applyUserInput(title,input)
    content[title] = newContent
    pp = generatePresentation(titles, content, images)
        
    # RENDER VIDEO
    os.startfile(pp)
    
    
def getTopic():
    global topic
    return topic

def getTitles():
    global titles
    return titles

def getContent(title):
    global content
    return content[title]


def getOptTitle():
    global optionalTitle
    return optionalTitle

def getSuggestion():
    global suggestion
    return suggestion

    
    # flask --app flaskr --debug run  
    # requests
    # openai
    # python-pptx
    #pexels_api