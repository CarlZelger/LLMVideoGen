import requests
import time

url = "https://apis.elai.io/api/v1/videos/from-presentation"
filepath = "test.pptx"
headers = {
    "Authorization": "Bearer VymX9HA3OH421WvWrp3o7ZfjNoF91tQK"
}

with open(filepath, 'rb') as file:
    files = {'file': file}
    #creates video from pptx File
    response = requests.post(url, headers=headers, files=files)
    print(response)

    if response.status_code == 200:
      video_id = response.content.decode('utf-8')
      print(video_id)
      url = "https://apis.elai.io/api/v1/videos/render/" + video_id[1:-1]

      headers = {
          "accept": "application/json",
          "Authorization": "Bearer VymX9HA3OH421WvWrp3o7ZfjNoF91tQK"
      }
      #Renders the video
      response = requests.post(url, headers=headers)

      print(response.text)
      if response.status_code == 200:
        url = "https://apis.elai.io/api/v1/videos/" + video_id[1:-1]

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer VymX9HA3OH421WvWrp3o7ZfjNoF91tQK"
        }
        #Retrieves the video
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
          print(response)
          while(response.status_code == 200 and  response.json().get('url') != None):
            print(response['status'])
            time.sleep(10)
            response = requests.get(url, headers=headers)

          print("render done!")
          video_data = response.json()  # Assuming the response is in JSON format
          video_url = video_data.get('url')  # Adjust the key based on actual response

          # Download the video
          if video_url:
              video_response = requests.get(video_url)
              with open('downloaded_video.mp4', 'wb') as f:
                  f.write(video_response.content)
              print("Video downloaded successfully!")
          else:
              print("No video URL found in the response")
        else:
            print("Failed to retrieve video:", response.status_code)
      else:
        print("Render failed")
