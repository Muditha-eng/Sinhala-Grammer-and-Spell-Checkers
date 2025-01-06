import tkinter as tk
from tkinter import scrolledtext

# Embedded corrections data
corrections_data = {
   "මම": {
        "ගියෙමු": "ගියෙමි",
        "ගියහ": "ගියෙමි",
        "ගියෝය": "ගියෙමි",
        "කලේය": "කලෙමි",
        "කලෙමු": "කලෙමි",
        "කීවෝය": "කීවෙමි",
        "කීවේය": "කීවෙමි",
        "යමු": "යමි"
    },
    "අපි": {
        "ගියෙමි": "ගියෙමු",
        "ගියහ": "ගියෙමු",
        "කලේය": "කලෙමු",
        "කලෝය": "කලෙමු",
        "කීවෝය": "කීවෙමු",
        "යමි": "යමු"
    },
    "අක්කා,අම්මා": {
        "ගියෙමි": "ගියාය",
        "ගියහ": "ගියාය",
        "කලේය": "කලාය",
        "කීවෝය": "කීවාය"
    },
    "මල්ලී": {
        "ගියෙමි": "ගියේය",
        "ගියහ": "ගියේය",
        "කලේය": "කලේය",
        "කීවෝය": "කීවේය"
    }
}

sinhala_words = {
    "\u0db8\u0dd9", "\u0d85\u0db4\u0dd2", "\u0d85\u0d9a\u0dca\u0d9a\u0dcf", "\u0d85\u0d9a\u0dca\u0d9a\u0dcf", "\u0d85\u0db9\u0dd0\u0dc0\u0dcf"
}


def correct_sentence_with_rules(sentence, corrections_data):
    """
    Corrects Sinhala grammar errors in a given sentence based on subject-specific rules.
    """
    words = sentence.split()
    if not words:
        return sentence

    subject = words[0]
    corrections = {}
    for key, rules in corrections_data.items():
        if subject in key.split(","):
            corrections = rules
            break

    corrected_sentence = sentence
    for incorrect, correct in corrections.items():
        if incorrect in sentence:
            corrected_sentence = sentence.replace(incorrect, correct)
            break

    return corrected_sentence


def validate_words(sentence, sinhala_words):
    """
    Validate words in the sentence against the Sinhala dictionary.
    """
    words = sentence.split()
    unknown_words = [word for word in words if word not in sinhala_words]
    return unknown_words


def process_sentence():
    sentence = input_box.get("1.0", tk.END).strip()

    if not sentence:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "Please enter a sentence.")
        return

    # Correct the sentence
    corrected_sentence = correct_sentence_with_rules(sentence, corrections_data)

    # Validate words
    unknown_words = validate_words(sentence, sinhala_words)

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"Original: {sentence}\n")
    output_box.insert(tk.END, f"Corrected: {corrected_sentence}\n")
    if unknown_words:
        output_box.insert(tk.END, f"Unknown words: {', '.join(unknown_words)}\n")


# Create the main application window
app = tk.Tk()
app.title("Sinhala Grammar Correction")
app.geometry("600x400")

# Input box
input_label = tk.Label(app, text="Enter a Sinhala sentence:")
input_label.pack()

input_box = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=70, height=10)
input_box.pack(pady=5)

# Correct button
correct_button = tk.Button(app, text="Correct", command=process_sentence)
correct_button.pack(pady=10)

# Output box
output_label = tk.Label(app, text="Output:")
output_label.pack()

output_box = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=70, height=10, state=tk.NORMAL)
output_box.pack(pady=5)

# Run the application
app.mainloop()
