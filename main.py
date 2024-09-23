import datetime
from gtts import gTTS
import subprocess
import os
import random


def load_dictionary():
    with open('words.txt') as f:
        lines = f.readlines()
        return lines


def speak(word):
    filepath = "sounds/" + word + ".mp3"
    if not os.path.isfile(filepath):
        # Language in which you want to convert
        language = 'en'

        # Creating a gTTS object
        tts = gTTS(text=word, lang=language, slow=False)

        # Saving the converted audio in a mp3 file
        tts.save(filepath)

    # Optionally, play the sound (works on some systems)
    # Use "open" on macOS and "xdg-open" on Linux
    # subprocess.Popen(["vlc", "--intf", "dummy", "--play-and-exit", filepath])
    os.system("vlc --intf dummy --play-and-exit " + filepath)


def getNextWord(dictionary, selected):
    # Text to be converted to speech
    word = random.sample(dictionary, 1)

    while (word[0].strip() in selected):
        word = random.sample(dictionary, 1)

    return word[0].strip()


def saveResults(selected, missed_words):
    filename = "reports/" + datetime.datetime.now().strftime("%y%m%d_%H%M%S") + ".txt"
    with open(filename, 'w') as f:
        f.write('-------------------------------\n')
        f.write("Words Tested (" + str(len(selected)) + ")\n")
        f.write('-------------------------------\n')
        for line in selected:
            f.write(line)
            f.write('\n')

        f.write('\n\n-------------------------------\n')
        f.write("Words to Practice (" + str(len(missed_words)) + ")\n")
        f.write('-------------------------------\n')
        for line in missed_words:
            f.write(line)
            f.write('\n')

    print("Report Saved to:", filename)


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------
correct = 0
incorrect = 0

dictionary = load_dictionary()
selected = []
missed_words = []

number_of_words = int(input("How many words to spell: "))

for i in range(number_of_words):
    word_to_spell = getNextWord(dictionary, selected)
    selected.append(word_to_spell)
    speak(word_to_spell)

    print("\n----------------------------------")
    print("Word", i+1, "of", number_of_words)
    print("----------------------------------")
    attempt = input("Spell the Word (Enter 'r' to repeat the word): ")

    # Allows you to hear it again
    while (attempt == 'r'):
        speak(word_to_spell)
        attempt = input("\nSpell the Word (Enter 'r' to hear it again): ")

    # Compares
    if (attempt.strip().lower() == word_to_spell):
        print("CORRECT\n")
        correct += 1
    else:
        print("INCORRECT.  The correct spelling is ", word_to_spell, "\n")
        incorrect += 1
        missed_words.append(word_to_spell + " (You typed: " + attempt + ")")

print("---------------------------------------------------")
print("RESULTS")
print("---------------------------------------------------")
print(correct, "correct;", incorrect, "incorrect\n")

saveResults(selected, missed_words)

print("\nDo better.  Be Asian.  Represent.")
