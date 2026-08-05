# voice-to-voice-ai-task
-------
This code listens to an audio question, asks an AI for the answer, and then speaks the answer out loud. 

## The 3 Steps Explained:

1. **Audio to Text (Step 1):** The code takes an audio file (input.wav). It cleans the audio format and uses Google to turn the spoken words into text. 
2. **AI Response (Step 2):** The text question is sent to Cohere AI. The AI reads the question and writes an answer.
3. **Text to Audio (Step 3):** The AI's written answer is sent to Google Text-to-Speech. This turns the text into a real voice and saves it as an MP3 file (output.mp3).
