import requests
import api_secrets
import time
import json

#upload file to Assembly API  and get response
filename = "Recording.m4a"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization': api_secrets.API_KEY}


CHUNK_SIZE = 5_242_880 
def upload(filename):  
    def read_file( filename):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(CHUNK_SIZE)
                if not data:
                    break
                yield data
    response = requests.post(upload_endpoint,
                        headers=headers,
                        data=read_file(filename))
    audio_url = response.json()['upload_url']
    return audio_url


#get transcript from Assembly API

def transcribe(audio_url,sentiment_analysis):
    json = { "audio_url": audio_url,'sentiment_analysis':sentiment_analysis} 
    response = requests.post(transcript_endpoint, json=json, headers=headers)
    return response.json()['id']



#poll



def poll(job_id):
    polling_endpoint = "https://api.assemblyai.com/v2/transcript/{}".format(job_id)
    polling_res =requests.get(polling_endpoint, headers=headers)
    return polling_res.json()


def get_transcription_result_url(url,sentiment_analysis):
    transcribe_id = transcribe(url,sentiment_analysis)
    while True:
        data = poll(transcribe_id)
        if data['status']=='completed':
            return data,None
        elif data['status']=='error':
            return data,data['error']
        
        print("Wating for transcription")
        time.sleep(30)

def save_transcript(url,title,sentiment_analysis=False):
    data,error = get_transcription_result_url(url,sentiment_analysis)
    if data:
        text_filename = title + ".txt"
        with open(text_filename, 'w') as f:
            f.write(data['text'])
        
        if sentiment_analysis:
            filename= title + "_sentiments.json"
            with open(filename, 'w') as f:
                sentiments = data['sentiment_analysis_results']
                json.dump(sentiments, f,indent=4)
        print("Transcription saved")
        return True
    elif error:
        print("Error!!",error)
        return False
