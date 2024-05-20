from flask import Flask, render_template, request, session
from flask_session import Session
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

openai.api_key = os.getenv("API")

@app.route("/", methods=["GET", "POST"])
def home():
    # Reset the session messages on page load
    if request.method == "GET":
        session.pop("messages", None)
    
    if "messages" not in session:
        session["messages"] = [{"role": "system", "content": "Creative teacher specialising in Design Thinking on Project Based Learning"}]

    if request.method == "POST":
        user_input = request.form["message"]
        session["messages"].append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=session["messages"]
        )
        reply = response["choices"][0]["message"]["content"]
        session["messages"].append({"role": "assistant", "content": reply})
        session.modified = True  # Ensure the session is saved

    return render_template("index.html", messages=session["messages"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
