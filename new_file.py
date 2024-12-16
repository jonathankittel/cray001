print("hello")
import torch
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
print("GPU Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU found")

Great idea! Let’s extend your Flask app to include a second page and use TypeScript to interact with the user by retrieving text input.
Steps to Add a Second Page with TypeScript

    Modify the Flask Backend:
        Add a new route for the second page.
    Set Up the Second Page with HTML:
        Create an HTML file for the second page.
    Use TypeScript for User Input:
        Add a form where the user can input text, and use TypeScript to interact with the input.
    Serve the TypeScript Files:
        Compile TypeScript to JavaScript and serve it using Flask.

Step 1: Modify the Flask Backend

Update your Flask app (new_file.py) to add a second page:

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask and PyTorch!"

@app.route('/second')
def second_page():
    return render_template('second.html')  # Renders the second page

if __name__ == '__main__':
    app.run(debug=True)