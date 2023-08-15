import openai
import speech_recognition as sr
import pyttsx3 as tts
from threading import Thread
import sys

class Assistant:
    def __init__(self, name):
        self.name = name
        self.recognizer = sr.Recognizer()

    def initiate_response(self, user_input):
        sample_output = '''Sample request: Hey ChatGPT! Can you tell me what Python is?
        
        Sample output: Python is a computer programming language often used to build websites and software, automate tasks, and conduct data analysis. Python is a general-purpose language, meaning it can be used to create a variety of different programs and isn't specialized for any specific problems.
        '''
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            stream=True,
            messages=[
                {"role": "system", "content": f"You are a personalized, helpful assistant called Bob that will respond to the user's query. If possible, try to keep responses short. This is a sample response: {sample_output}"},
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

    def speak(self, message):
        engine = tts.init()
        engine.setProperty('voice', 'com.apple.eloquence.en-US.Eddy')
        engine.setProperty('rate', 175)
        engine.say(message)

    def run_assistant(self):
        recognizer = sr.Recognizer()
        while True:
            try:
                with sr.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)
                    text = recognizer.recognize_google(audio)
                    # print(text)
                    if text == 'stop' or text == 'bye' or text == 'Bye':
                        self.speak('Bye! Talk to you next time.')
                    else:
                        if text is not None:
                            pass
            except:
                print("Listening...")
                continue
