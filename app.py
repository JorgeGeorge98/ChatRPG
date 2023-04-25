from os import environ

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = environ["OPENAI_API_KEY"]


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Image.create(
            prompt=generate_prompt(animal),
            n=1,
            size="1024x1024"
        )
        return redirect(url_for("index", result=response['data'][0]['url']))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )



#def index():
#    if request.method == "POST":
#        animal = request.form["animal"]
#        response = openai.Image.create(
#            prompt=generate_prompt(animal),
#            n=1,
#            size="1024x1024"
#        )
#        return redirect(url_for("index", result=response['data'][0]['url']))

#    result = request.args.get("result")
#    return render_template("index.html", result=result)


