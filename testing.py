from gtts import gTTS
import os

# Text to be converted to voice
text = "Hello, welcome to the world of Python programming!"

# Language in which you want to convert
language = 'en'

# Creating an object of gTTS
speech = gTTS(text=text, lang=language, slow=False)

# Saving the converted audio in a mp3 file
speech.save("output.mp3")

# Playing the converted file (works on Windows)
os.system("start output.mp3")
