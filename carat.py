import pyttsx3
import speech_recognition as sr
from datetime import datetime
import webbrowser
import urllib.parse
import subprocess
import os
import ast
import operator


# ============================================================
# CARAT AI ASSISTANT
# ============================================================

print("==========================================")
print("          CARAT AI ASSISTANT")
print("==========================================")


# ============================================================
# VOICE ENGINE
# ============================================================

try:
    engine = pyttsx3.init("sapi5")

    voices = engine.getProperty("voices")

    if voices:
        engine.setProperty("voice", voices[0].id)

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

except Exception as error:
    print("Voice engine error:", error)
    engine = None


# ============================================================
# SPEECH RECOGNITION
# ============================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


# ============================================================
# SPEAK
# ============================================================

def speak(text):

    print("CARAT:", text)

    if engine is not None:

        try:
            engine.say(text)
            engine.runAndWait()

        except Exception as error:
            print("Speech error:", error)


# ============================================================
# LISTEN
# ============================================================

def listen():

    try:

        with sr.Microphone() as source:

            print()
            print("Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            try:

                audio = recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=7
                )

            except sr.WaitTimeoutError:

                print("CARAT: No speech detected.")
                return ""

        print("Recognizing...")

        try:

            text = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("YOU:", text)

            return text.lower().strip()

        except sr.UnknownValueError:

            print("CARAT: I could not understand that.")
            return ""

        except sr.RequestError:

            print("CARAT: Internet speech recognition is unavailable.")
            return ""

    except OSError as error:

        print("Microphone error:", error)

        speak(
            "I cannot access the microphone. "
            "Please check your microphone settings."
        )

        return ""

    except Exception as error:

        print("Listening error:", error)
        return ""


# ============================================================
# OPEN WINDOWS APPLICATIONS
# ============================================================

def open_application(application):

    try:

        if application == "notepad":

            subprocess.Popen("notepad.exe")

            speak("Opening Notepad.")


        elif application == "calculator":

            subprocess.Popen("calc.exe")

            speak("Opening Calculator.")


        elif application == "paint":

            subprocess.Popen("mspaint.exe")

            speak("Opening Paint.")


        elif application == "command prompt":

            subprocess.Popen("cmd.exe")

            speak("Opening Command Prompt.")


        elif application == "file explorer":

            subprocess.Popen("explorer.exe")

            speak("Opening File Explorer.")


        else:

            speak("I don't know that application yet.")

    except Exception as error:

        print("Application error:", error)

        speak("I could not open that application.")


# ============================================================
# GOOGLE SEARCH
# ============================================================

def google_search(search_text):

    try:

        if not search_text:

            speak("What would you like me to search for?")
            return

        speak("Searching for " + search_text)

        encoded_text = urllib.parse.quote(search_text)

        url = (
            "https://www.google.com/search?q="
            + encoded_text
        )

        webbrowser.open(url)

    except Exception as error:

        print("Search error:", error)

        speak("I could not perform the search.")


# ============================================================
# NOTES
# ============================================================

NOTES_FILE = "carat_notes.txt"


def take_note():

    speak("What would you like me to write down?")

    note = listen()

    if not note:
        speak("I did not hear the note.")
        return

    try:

        with open(
            NOTES_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            time_now = datetime.now().strftime(
                "%d-%m-%Y %I:%M %p"
            )

            file.write(
                "[" + time_now + "] "
                + note
                + "\n"
            )

        speak("Your note has been saved.")

    except Exception as error:

        print("Note error:", error)

        speak("I could not save your note.")


def read_notes():

    try:

        if not os.path.exists(NOTES_FILE):

            speak("You do not have any saved notes yet.")
            return

        with open(
            NOTES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            notes = file.read().strip()

        if notes:

            print()
            print("========== CARAT NOTES ==========")
            print(notes)
            print("=================================")

            speak("I found your saved notes.")

        else:

            speak("Your notes file is empty.")

    except Exception as error:

        print("Read notes error:", error)

        speak("I could not read your notes.")


# ============================================================
# SAFE CALCULATOR
# ============================================================

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow
}


def calculate_expression(expression):

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        def calculate(node):

            if isinstance(node, ast.Expression):

                return calculate(node.body)

            if isinstance(node, ast.Constant):

                if isinstance(
                    node.value,
                    (int, float)
                ):

                    return node.value

                raise ValueError()

            if isinstance(node, ast.BinOp):

                left = calculate(node.left)
                right = calculate(node.right)

                operation = operators.get(
                    type(node.op)
                )

                if operation is None:
                    raise ValueError()

                return operation(
                    left,
                    right
                )

            if isinstance(node, ast.UnaryOp):

                value = calculate(node.operand)

                if isinstance(
                    node.op,
                    ast.USub
                ):

                    return -value

                if isinstance(
                    node.op,
                    ast.UAdd
                ):

                    return value

                raise ValueError()

            raise ValueError()

        result = calculate(tree)

        return result

    except Exception:

        return None


def calculator():

    speak(
        "What calculation would you like me to perform?"
    )

    expression = listen()

    if not expression:
        return

    expression = expression.replace(
        "plus",
        "+"
    )

    expression = expression.replace(
        "minus",
        "-"
    )

    expression = expression.replace(
        "times",
        "*"
    )

    expression = expression.replace(
        "multiplied by",
        "*"
    )

    expression = expression.replace(
        "divided by",
        "/"
    )

    expression = expression.replace(
        "divide",
        "/"
    )

    expression = expression.replace(
        "x",
        "*"
    )

    expression = expression.replace(
        " ",
        ""
    )

    result = calculate_expression(
        expression
    )

    if result is None:

        speak(
            "Sorry, I could not calculate that."
        )

    else:

        speak(
            "The answer is "
            + str(result)
        )


# ============================================================
# USEFUL COMMANDS
# ============================================================

def show_help():

    print()
    print("========== CARAT COMMANDS ==========")
    print("Hello")
    print("What is the time")
    print("What is the date")
    print("Search for Python")
    print("Open Google")
    print("Open YouTube")
    print("Open GitHub")
    print("Open Notepad")
    print("Open Calculator")
    print("Open Paint")
    print("Open File Explorer")
    print("Take a note")
    print("Read my notes")
    print("Calculate")
    print("Who are you")
    print("What is your name")
    print("Help")
    print("Stop")
    print("====================================")
    print()

    speak(
        "I have displayed the commands "
        "that I currently understand."
    )


# ============================================================
# COMMAND PROCESSING
# ============================================================

def process_command(command):

    try:

        # -------------------------
        # GREETING
        # -------------------------

        if (
            "hello" in command
            or "hi" in command
            or "hey" in command
        ):

            speak(
                "Hello Tharun. How can I help you?"
            )


        # -------------------------
        # TIME
        # -------------------------

        elif "time" in command:

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            speak(
                "The current time is "
                + current_time
            )


        # -------------------------
        # DATE
        # -------------------------

        elif "date" in command:

            current_date = datetime.now().strftime(
                "%d %B %Y"
            )

            speak(
                "Today's date is "
                + current_date
            )


        # -------------------------
        # GOOGLE
        # -------------------------

        elif "open google" in command:

            speak("Opening Google.")

            webbrowser.open(
                "https://www.google.com"
            )


        # -------------------------
        # YOUTUBE
        # -------------------------

        elif "open youtube" in command:

            speak("Opening YouTube.")

            webbrowser.open(
                "https://www.youtube.com"
            )


        # -------------------------
        # GITHUB
        # -------------------------

        elif "open github" in command:

            speak("Opening GitHub.")

            webbrowser.open(
                "https://github.com"
            )


        # -------------------------
        # SEARCH
        # -------------------------

        elif command.startswith(
            "search for"
        ):

            search_text = command.replace(
                "search for",
                "",
                1
            ).strip()

            google_search(search_text)


        elif command.startswith(
            "search"
        ):

            search_text = command.replace(
                "search",
                "",
                1
            ).strip()

            google_search(search_text)


        # -------------------------
        # NOTEPAD
        # -------------------------

        elif "open notepad" in command:

            open_application(
                "notepad"
            )


        # -------------------------
        # CALCULATOR APP
        # -------------------------

        elif (
            "open calculator" in command
            or "open calc" in command
        ):

            open_application(
                "calculator"
            )


        # -------------------------
        # PAINT
        # -------------------------

        elif "open paint" in command:

            open_application(
                "paint"
            )


        # -------------------------
        # COMMAND PROMPT
        # -------------------------

        elif (
            "open command prompt" in command
            or "open cmd" in command
        ):

            open_application(
                "command prompt"
            )


        # -------------------------
        # FILE EXPLORER
        # -------------------------

        elif (
            "open file explorer" in command
            or "open explorer" in command
        ):

            open_application(
                "file explorer"
            )


        # -------------------------
        # TAKE NOTE
        # -------------------------

        elif (
            "take a note" in command
            or "take note" in command
            or "write a note" in command
            or "save a note" in command
        ):

            take_note()


        # -------------------------
        # READ NOTES
        # -------------------------

        elif (
            "read my notes" in command
            or "show my notes" in command
            or "read notes" in command
        ):

            read_notes()


        # -------------------------
        # CALCULATOR
        # -------------------------

        elif (
            "calculate" in command
            or "do a calculation" in command
        ):

            calculator()


        # -------------------------
        # HELP
        # -------------------------

        elif "help" in command:

            show_help()


        # -------------------------
        # WHO ARE YOU
        # -------------------------

        elif (
            "who are you" in command
            or "what are you" in command
        ):

            speak(
                "I am CARAT, your personal Python voice assistant."
            )


        # -------------------------
        # NAME
        # -------------------------

        elif "your name" in command:

            speak(
                "My name is CARAT."
            )


        # -------------------------
        # STOP
        # -------------------------

        elif (
            "stop" in command
            or "exit" in command
            or "quit" in command
            or "goodbye" in command
        ):

            speak(
                "Goodbye Tharun. See you again."
            )

            return False


        # -------------------------
        # UNKNOWN COMMAND
        # -------------------------

        else:

            speak(
                "Sorry, I don't know that command yet. "
                "Say help to see my commands."
            )

    except Exception as error:

        print()
        print("Command processing error:", error)

        speak(
            "Something went wrong while processing that command."
        )

    return True


# ============================================================
# START CARAT
# ============================================================

speak(
    "Hello Tharun. "
    "I am CARAT, your personal AI assistant. "
    "My systems are ready."
)


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    command = listen()

    if command:

        should_continue = process_command(
            command
        )

        if not should_continue:

            break


# ============================================================
# SHUTDOWN
# ============================================================

print()
print("==========================================")
print("       CARAT HAS BEEN STOPPED")
print("==========================================")