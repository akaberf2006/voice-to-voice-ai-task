import speech_recognition as sr
import cohere
from gtts import gTTS
import os
from pydub import AudioSegment

# --- Configuration ---
COHERE_API_KEY = 'API_KEY'
INPUT_AUDIO_FILE = 'input.mp3'
OUTPUT_AUDIO_FILE = 'output.mp3'

co = cohere.Client(COHERE_API_KEY)


def step_1_audio_to_text(audio_path):
    print("Step 1: Converting Audio to Text...")
    recognizer = sr.Recognizer()

    clean_audio_path = "clean_temp.wav"
    try:
        print(f"Cleaning audio file format...")
        audio = AudioSegment.from_file(audio_path)
        audio.export(clean_audio_path, format="wav")
    except Exception as e:
        print(f"Error converting audio file: {e}")
        return None

    try:
        with sr.AudioFile(clean_audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized Text: '{text}'")
            os.remove(clean_audio_path)
            return text
    except FileNotFoundError:
        print(f"Error: Could not find the file {audio_path}.")
        return None
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return None


def step_2_generate_llm_response(prompt_text):
    print("\nStep 2: Generating response using Cohere LLM...")
    try:
        response = co.chat(
            model='command-r-08-2024', 
            message=prompt_text,
            temperature=0.7
        )
        llm_text = response.text.strip()
        print(f"LLM Response: '{llm_text}'")
        return llm_text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None


def step_3_text_to_audio(text, output_path):
    print("\nStep 3: Converting Text to Audio...")
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        print(f"Success! Audio saved as {output_path}")
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    user_text = step_1_audio_to_text(INPUT_AUDIO_FILE)

    if user_text:
        bot_response = step_2_generate_llm_response(user_text)

        if bot_response:
            step_3_text_to_audio(bot_response, OUTPUT_AUDIO_FILE)
