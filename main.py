import openai
import pyttsx3 as tts
import pyaudio
from threading import Thread
from queue import Queue
from datetime import datetime
import speech_recognition as sr
import sys

# Code to request 

def speak():
    pass

def transcribe(audio_file):
    # Use Whisper API (transcribe audio_file)
    pass

def initiate_response(user_input):
    sample_output = '''Sample request: Hey ChatGPT! Can you tell me what Python is?
    
    Sample output: Python is a computer programming language often used to build websites and software, automate tasks, and conduct data analysis. Python is a general-purpose language, meaning it can be used to create a variety of different programs and isn't specialized for any specific problems.
    '''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        stream=True,
        messages=[
            {"role": "system", "content": f"You are a personalized, helpful assistant that will answer any questions and respond to the user's query. If possible, try to keep responses short. This is a sample response: {sample_output}"},
            {"role": "user", "content": user_input}
        ]
    )
    # return response["choices"][0]["message"]["content"]
    result = ""
    for chunk in response:
        data = chunk['choices'][0]
        if data['finish_reason'] is not None:
            break
        # print(data['delta']['content'], end=" ")
        result += data['delta']['content']
    return result

def final_response(input_text):
    engine = tts.init()
    engine.setProperty('voice', 'com.apple.eloquence.en-US.Eddy')
    engine.setProperty('rate', 175)
    engine.say(input_text)
    engine.runAndWait()

temp_key = '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'
openai.api_key = temp_key

def main():
    openai.api_key = temp_key
    user = initiate_response("맥북의 역사에 대해서 간략하게 설명해주세요")
    final_response(user)
    print("Finished!")
    return True

## Testing Features

def test_speak():
    engine = tts.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'com.apple.voice.compact.ko-KR.Yuna')
    engine.setProperty('rate', 175)
    for voice in voices:
        print(f"Voice: {voice.name} {voice.id}")
    engine.say("Hey! This is a text-to-speech test!")
    engine.runAndWait()

def test_record():
    print("Begin")
    engine = tts.init()
    engine.setProperty('voice', 'com.apple.eloquence.en-US.Eddy')
    engine.setProperty('rate', 175)
    recognizer = sr.Recognizer()
    print("Recognizer initialized")
    while True:
        try:
            with sr.Microphone() as mic:
                print("Recording...")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                text = recognizer.recognize_google(audio)
                print(text)
                if text == "stop" or text == "Bye":
                    engine.say("Bye! If you have any other questions please ask.")
                    engine.runAndWait()
                    engine.stop()
                    sys.exit()
                else:
                    if text is not None:
                        response = initiate_response(text)
                        try:
                            engine.say(response)
                            engine.runAndWait()
                            continue
                        except:
                            print("Can't run response")
                # if "Hey GPT" in text:
                #     audio = recognizer.listen(mic)
                #     text = recognizer.recognize_google(audio)
                #     text = text.lower()
                #     print(text)
                #     if text == "stop" or text == "Bye":
                #         engine.say("Bye")
                #         engine.runAndWait()
                #         engine.stop()
                #         sys.exit()
                #     else:
                #         if text is not None:
                #             response = final_response(text)
                #             if response is not None:
                #                 engine.say(response)
                #             else:
                #                 engine.say("Invalid prompt")
                #                 engine.runAndWait()
        except:
            print("Exception")
            continue


## Final Runs
# final_response(initiate_response("Tell me a brief short self-introduction"))

# test_speak()

test_record()