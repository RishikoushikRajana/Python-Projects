import pyttsx3
import datetime
import webbrowser
import os
import time  # For slight pauses if needed


def speak(text):
    try:
        engine = pyttsx3.init()

        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error during text-to-speech: {e}")
        print("Please ensure your system has a text-to-speech engine installed.")


def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your simple text-based voice assistant. How can I help you today?")


def process_command(command):

    command = command.lower()

    if "hello" in command or "hi" in command:
        speak("Hello there!")
    elif "how are you" in command:
        speak("I am doing well, thank you for asking!")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
    elif "search" in command:
        speak("What would you like me to search for on Google?")
        search_query = input("Type your search query: ").strip()
        if search_query:
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            speak(f"Here's what I found for {search_query} on Google.")
        else:
            speak("No search query provided.")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "who are you" in command:
        speak("I am a simple voice assistant, created with Python.")
    elif "what can you do" in command:
        speak(
            "I can tell you the time and date, open websites like Google and YouTube, and search for things on Google.")
    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        return True
    else:
        speak("I'm sorry, I don't know how to do that yet.")
    return False


def main():
    greet()
    while True:
        user_command = input("\nEnter your command (type 'exit' to quit): ").strip()

        if not user_command:
            speak("Please enter a command.")
            continue

        if process_command(user_command):
            break


if __name__ == "__main__":
    main()