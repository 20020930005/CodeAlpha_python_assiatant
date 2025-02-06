import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import pyjokes
import datetime
import webbrowser
from transformers import pipeline
import time

# Initialize the speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change to voices[1].id for female voice

# Initialize Hugging Face Question Answering model
question_answerer = pipeline("question-answering")

def talk(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen to user command and return as text."""
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=100)  # Increase timeout to 10 seconds (or adjust as needed)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"User said: {command}")
            return command
    except Exception as e:
        print(f"Error: {e}")
        return "I couldn't understand you."

def get_answer(question, context):
    """Use Hugging Face model to answer a question based on the given context."""
    response = question_answerer(question=question, context=context)
    return response['answer']

def run_assistant():
    """Main function to run the assistant."""
    command = take_command()

    # Greet the user once when starting
    if "hello" in command: 
        talk("Hello there! How can I assist you today?")
        time.sleep(1)  # A small pause before listening for the next command

    elif "good morning" in command:
        talk("good morning how can i assist you")


    elif "good evening" in command:
        talk("good morning how can i assist you")

    # Play a song
    elif "play" in command:
        song = command.replace("play", "").strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)

    # Get current time
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        talk(f"The current time is {current_time}")

    # Get information about a person from Wikipedia
    elif "who is" in command:
        person = command.replace("who is", "").strip()
        try:
            info = wikipedia.summary(person, 1)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"There are multiple results for {person}, please be more specific.")
        except wikipedia.exceptions.HTTPTimeoutError:
            talk("I couldn't fetch the information at the moment. Please try again later.")

    # Tell a joke
    elif "joke" in command:
        joke = pyjokes.get_joke()
        talk(joke)

    # Placeholder for weather info
    elif "weather" in command:
        talk("Sorry, I cannot provide weather information right now.")

    # Search for something on Google
    elif "search" in command:
        search_term = command.replace("search", "").strip()
        talk(f"Searching for {search_term}")
        pywhatkit.search(search_term)

    # Open a website
    elif "open" in command:
        website = command.replace("open", "").strip()
        talk(f"Opening {website}")
        webbrowser.open(f"https://{website}.com")

    # Answer general questions based on context
    elif "ask" in command or "question" in command:
        question = command.replace("ask", "").replace("question", "").strip()
        context = "The capital of France is Paris. Paris is known for its rich culture, art, and history."  # Example context
        answer = get_answer(question, context)
        talk(f"The answer is: {answer}")

    # Greet the user in different scenarios
    elif "good morning" in command:
        talk("Good morning! How can I help you today?")
    
    elif "good evening" in command:
        talk("Good evening! What can I do for you?")
    
    elif "how are you" in command:
        talk("I'm doing great, thank you for asking! How are you?")
    
    elif "thank you" in command:
        talk("You're welcome! Let me know if you need anything else.")

    elif "good" in command:
        talk("Happy to hear that")

    elif "let's do" in command:
        talk("Sure, what do you want to do?")

    elif "sorry" in command:
        talk("No problem! How can I assist you further?")
    
    elif "what is your name" in command:
        talk("I am your voice assistant. How can I help you today?")

    elif "idiot" in command:
        talk("I am extremely sorry I am not that advanced")

    elif "oh my god" in command:
        talk("I am sorry")

    elif "i am" in command:
        talk(f"Hello dear")

    elif "i can't repeat" in command:
        talk("I am sorry, I try my best")

    elif "i am alone" in command:
        talk("Don't worry, I am here to talk with you, dear")

    elif "technological trends" in command:
        talk("In 2025, we see AI and Gen AI having a major impact on companies' priorities and also on many adjacent technology domains, such as robotics, supply chains, or tomorrow's energy mix. In today's fast-paced business environment, understanding emerging technologies is essential for future planning.")

    elif "explain" in command:
        talk("I am sorry, I don't have that much wide knowledge.")

    elif "can you" in command:
        talk("Yeah, I think I can do")
    
    elif "bye" in command or "exit" in command:
        talk("Goodbye! Have a great day!")
        return False  # Stops the loop

    # Fallback for unknown commands
    else:
        talk("I didn't understand that. Can you say it again?")
    
    return True

# Run the assistant in a loop
while True:
    if not run_assistant():
        break  # Breaks the loop when "exit" or "bye" is said

