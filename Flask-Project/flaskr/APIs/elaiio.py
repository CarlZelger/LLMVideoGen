import requests
import time

def render(fp):
    url = "https://apis.elai.io/api/v1/videos/from-presentation"
    filepath = fp
    headers = {
        "Authorization": "Bearer VymX9HA3OH421WvWrp3o7ZfjNoF91tQK"
    }

    with open(filepath, 'rb') as file:
        files = {'file': file}
        # creates video from pptx File
        response = requests.post(url, headers=headers, files=files)
        print("Initial response status:", response.status_code)
        print("Initial response content:", response.text)

        if response.status_code == 200:
            video_id = response.content.decode('utf-8').strip('"')
            print("Video ID:", video_id)
            url = f"https://apis.elai.io/api/v1/videos/render/{video_id}"

            headers = {
                "accept": "application/json",
                "Authorization": "Bearer VymX9HA3OH421WvWrp3o7ZfjNoF91tQK"
            }
            # Renders the video
            response = requests.post(url, headers=headers)
            print("Render response status:", response.status_code)
            print("Render response content:", response.text)
            
            if response.status_code == 200:
                url = f"https://apis.elai.io/api/v1/videos/{video_id}"

                headers = {
                    "accept": "application/json",
                    "Authorization": "Bearer VymX9HA3OH421WvWrp3o7ZfjNoF91tQK"
                }
                # Retrieves the video
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    while response.status_code == 200 and response.json().get('url') is None:
                        print("Waiting for video rendering to complete...")
                        time.sleep(10)
                        response = requests.get(url, headers=headers)
                        data = response.json().get('data', {})
                        app_error = data.get('appError')
                        print("Video retrieval appError:", app_error)

                    if response.status_code == 200:
                        print("Rendering complete!")
                        video_data = response.json()
                        video_url = video_data.get('url')

                        # Download the video
                        if video_url:
                            video_response = requests.get(video_url)
                            with open('downloaded_video.mp4', 'wb') as f:
                                f.write(video_response.content)
                            print("Video downloaded successfully!")
                            return 'downloaded_video.mp4'
                        else:
                            print("No video URL found in the response")
                    else:
                        print("Failed to retrieve video:", response.status_code)
                else:
                    print("Failed to retrieve video:", response.status_code)
            else:
                print("Failed to render video:", response.status_code)
        else:
            print("Failed to upload and process presentation:", response.status_code)
        return "error"

# render("C:\\TUGraz\\BP\\LLMVideoGen\\Flask-Project\\test1.pptx")
# render("C:\\Users\\carlz\\OneDrive\\Desktop\\hghgl.pptx")