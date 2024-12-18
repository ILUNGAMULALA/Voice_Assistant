import speech_recognition as sr
import os
import google.generativeai as genai
import pyttsx3
import socket

ESP32_IP = "192.168.26.155"
ESP32_PORT = 80
genai.configure(api_key="AIzaSyDLZi6TiiFrH547uMVYZSx4Zpnl4_Yk7nM")

list_of_speeches = ["switch on the light","switch off the light" , "switch on the lights", "switch off the lights", "open the door", "close the door", "open the window", "close  the window"]

def send_command_to_esp32(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(100)  # Set a 5-second timeout (you can adjust this)
            s.connect((ESP32_IP, ESP32_PORT))
            s.sendall(f"{command}\n".encode())
            print("Command sent:", command)
    except socket.timeout:
        print("Connection timed out. ESP32 is not responding.")
    except Exception as e:
        print("An error occurred:", e)



def text_to_speech(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Get a list of all available voices
    voices = engine.getProperty('voices')

    # Set the voice to a feminine voice (typically, index 1 or 0 is feminine on most systems)
    engine.setProperty('voice', voices[1].id)  # Try voices[0] or voices[1] for female voices

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

    # Convert the text to speech
    engine.say(text)

    # Run the engine and wait for it to complete
    engine.runAndWait()
    engine.stop()


def gemini_api(word_to_search):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(word_to_search)

    print(response.text)

    text_to_speech(response.text)


def speech_to_text():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as input
    with sr.Microphone() as source:
        print("Please speak something...")

        try:
            # Listen to the speech
            audio = recognizer.listen(source)
            print("Processing...")

            # Use Google's speech recognition to convert to text
            text = recognizer.recognize_google(audio)

            if text in list_of_speeches:
                print("Daniel")
                #send_command_to_esp32(text)

            else:
                gemini_api(text)
                #print(f"Transcribed Text: {text}")

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")


### Send the text to Gemini


if __name__ == "__main__":
    speech_to_text()