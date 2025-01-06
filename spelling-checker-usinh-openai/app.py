import tkinter as tk
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Azure OpenAI endpoint and API key
openai.api_base = "https://models.inference.ai.azure.com"  # Replace with your Azure OpenAI endpoint
openai.api_key = os.getenv("GITHUB_TOKEN")

def submit_text():
    user_input = text_input.get("1.0", tk.END).strip()
    if not user_input:
        result_label.config(text="Please enter some text!", fg="red")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Replace with your specific model name
                               messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": """
                 
                 අපි බත් කනවා here now when the sentence is start with අපි , it must be end with මු, make the correct sentence 
                 
                 
                 """}
            ],
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
        response_text = response["choices"][0]["message"]["content"]
        result_label.config(text=response_text, fg="black")
    except Exception as e:
        result_label.config(text=f"An error occurred: {e}", fg="red")

# Create the main Tkinter window
root = tk.Tk()
root.title("Chat API UI")
root.geometry("600x600")

# Add widgets
label = tk.Label(root, text="Enter your text below:", font=("Arial", 12))
label.pack(pady=10)

text_input = tk.Text(root, height=10, width=50, wrap=tk.WORD)
text_input.pack(pady=10)

submit_button = tk.Button(root, text="Submit", command=submit_text, font=("Arial", 12), bg="#007bff", fg="white")
submit_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), wraplength=500, justify="left")
result_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
