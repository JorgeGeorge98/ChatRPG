from os import environ
import urllib
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = environ["OPENAI_API_KEY"]

story_begun = False
prompt = ""

@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")

@app.route('/fantasia', methods=("GET", "POST"))
def fantasia():
    global story_begun
    global prompt

    if request.method == "POST":
        userInput = request.form["userInput"]
        response = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=3000,
            prompt=generate_prompt(userInput, story_begun),
            temperature=1,
        )
        imgUrl = openai.Image.create(
            prompt=response.choices[0].text,
            n=1,
            size="256x256"
        )
        if not story_begun:
            story_begun = True
        return redirect(url_for("fantasia", result=response.choices[0].text, imgUrl=imgUrl['data'][0]['url']))

    result = request.args.get("result")
    imgUrl = request.args.get("imgUrl")
    if imgUrl is not None:
        decoded_url = urllib.parse.unquote(imgUrl)
    else:
        decoded_url = None
    
    return render_template("fantasia.html", result=result, imgUrl=decoded_url, story_begun=story_begun)

def generate_prompt(userInput, story_begun):

    if story_begun:
        return """Genera la continuacion de la historia de fantasia de una forma coherente

        Respuesta del usuario: {}
        Continuacion de la historia:""".format(userInput.capitalize())
    else:
        return """Comienza una historia de fantasia con el nombre que se introduce

        Nombre: Pepe
        Historia: Pepe caminaba por un bosque encantado cuando encontro a un ogro llamado Alexander, que hace pepe?
        Nombre: Jose
        Historia: Jose se a despertado en una mazmorra encadenado en un traje de cuero BDSM, a Jose le gusta, que hace jose?
        Nombre: {}
        Historia:""".format(userInput.capitalize())
