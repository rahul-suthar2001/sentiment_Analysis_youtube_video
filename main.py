import json
from yt_extract import get_video_info, get_audio_url
from api import save_transcript

def save_video_sentiments(url):
    video_infos = get_video_info(url)
    audio_url = get_audio_url(video_infos)
    title= video_infos["title"]
    title = title.strip().replace(" ", "_")

    title = "data/" + title 
    save_transcript(audio_url, title,sentiment_analysis=True)

if __name__=="__main__": 
    url  = input("Enter video url : ")
    save_video_sentiments(url)
