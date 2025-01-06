import re
from tkinter import Tk, Label, Entry, Button, Listbox, END, messagebox
from typing import List, Tuple
from Levenshtein import distance as edit_distance

class SinhalaSpellChecker:
    def __init__(self, dictionary_path: str):
        self.dictionary = self._load_dictionary(dictionary_path)
    
    def _load_dictionary(self, path: str) -> set:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return set(word.strip() for word in f if word.strip())
        except FileNotFoundError:
            print(f"Error: Dictionary file '{path}' not found.")
            return set()
    
    def suggest_corrections(self, word: str, max_suggestions: int = 5) -> List[Tuple[str, float]]:
        if not self.dictionary:
            print("Error: Dictionary is empty. Please load a valid dictionary.")
            return []

        if word in self.dictionary:
            return [(word, 1.0)]
        
        suggestions = []
        for dict_word in self.dictionary:
            dist = edit_distance(word, dict_word)
            similarity = 1 - (dist / max(len(word), len(dict_word)))
            if similarity > 0.6:
                suggestions.append((dict_word, similarity))
        
        return sorted(suggestions, key=lambda x: x[1], reverse=True)[:max_suggestions]

class SinhalaSpellCheckerUI:
    def __init__(self, root: Tk, spell_checker: SinhalaSpellChecker):
        self.spell_checker = spell_checker
        
        root.title("Sinhala Spell Checker")
        root.geometry("400x300")

        self.label = Label(root, text="Enter a Sinhala word:")
        self.label.pack(pady=10)

        self.entry = Entry(root, font=("Arial", 14))
        self.entry.pack(pady=5)

        self.check_button = Button(root, text="Check Spelling", command=self.check_spelling)
        self.check_button.pack(pady=10)

        self.result_label = Label(root, text="", fg="blue")
        self.result_label.pack(pady=10)

        self.suggestions_listbox = Listbox(root, font=("Arial", 12), width=40, height=10)
        self.suggestions_listbox.pack(pady=10)

    def check_spelling(self):
        word = self.entry.get().strip()

        if not word:
            messagebox.showwarning("Input Error", "Please enter a Sinhala word.")
            return

        if not re.match(r"^[\u0D80-\u0DFF]+$", word):
            messagebox.showerror("Input Error", "Please enter a valid Sinhala word.")
            return

        self.suggestions_listbox.delete(0, END)

        if word in self.spell_checker.dictionary:
            self.result_label.config(text=f"'{word}' is correctly spelled.", fg="green")
        else:
            self.result_label.config(text=f"'{word}' is misspelled.", fg="red")
            suggestions = self.spell_checker.suggest_corrections(word)

            if suggestions:
                for suggestion, score in suggestions:
                    self.suggestions_listbox.insert(END, f"{suggestion} (Similarity: {score:.2f})")
            else:
                self.suggestions_listbox.insert(END, "No suggestions available.")

if __name__ == "__main__":
    dictionary_path = "./data/sinhala_dictionary.txt"
    spell_checker = SinhalaSpellChecker(dictionary_path)

    root = Tk()
    app = SinhalaSpellCheckerUI(root, spell_checker)
    root.mainloop()
