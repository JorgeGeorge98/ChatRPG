from os import environ
import urllib
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = environ["OPENAI_API_KEY"]

@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")

@app.route('/fantasia', methods=("GET", "POST"))
def fantasia():
    if request.method == "POST":
        name = request.form["name"]
        response = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=3000,
            prompt=generate_prompt(name),
            temperature=1,
        )
        imgUrl = openai.Image.create(
            prompt=response.choices[0].text,
            n=1,
            size="256x256"
        )
        return redirect(url_for("fantasia", result=response.choices[0].text, imgUrl=imgUrl['data'][0]['url']))

    result = request.args.get("result")
    imgUrl = request.args.get("imgUrl")
    if imgUrl is not None:
        decoded_url = urllib.parse.unquote(imgUrl)
    else:
        decoded_url = None
    
    return render_template("fantasia.html", result=result, imgUrl=decoded_url)

def generate_prompt(name):
    return """Comienza una historia de fantasia con el nombre que se introduce

Nombre: Pepe
Historia: Pepe caminaba por un bosque encantado cuando encontro a un ogro llamado Alexander, que hace pepe?
Nombre: Jose
Historia: Jose se a despertado en una mazmorra encadenado en un traje de cuero BDSM, a Jose le gusta, que hace jose?
Nombre: {}
Historia:""".format(name.capitalize())
