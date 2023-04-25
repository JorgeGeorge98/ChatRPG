from os import environ

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = environ["OPENAI_API_KEY"]


@app.route("/", methods=("GET", "POST"))
#def index():
#    if request.method == "POST":
#        name = request.form["name"]
#        response = openai.Completion.create(
#            model="text-davinci-003",
#            max_tokens=2048,
#            prompt=generate_prompt(name),
#            temperature=1,
#        )
#        return redirect(url_for("index", result=response.choices[0].text))
#
#    result = request.args.get("result")
#    return render_template("index.html", result=result)

def index():
    if request.method == "POST":
        name = request.form["name"]
        response = openai.Image.create(
            prompt="Eustaquio estaba caminando a través de una profunda selva cuando de repente se encontró cara a cara con un enorme dragón. Eustaquio sabía cuales eran los resultados de enfrentarse con un dragón, pero tuvo un atisbo de valor y se preparó para lo que vendría a continuación. ¿Qué hace Eustaquio?",
            n=1,
            size="256x256"
        )
        return redirect(url_for("index", result=response['data'][0]['url']))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt(name):
    return """Comienza una historia de fantasia con el nombre que se introduce

Nombre: Pepe
Historia: Pepe caminaba por un bosque encantado cuando encontro a un ogro llamado Alexander, que hace pepe?
Nombre: Jose
Historia: Jose se a despertado en una mazmorra encadenado en un traje de cuero BDSM, a Jose le gusta, que hace jose?
Nombre: {}
Historia:""".format(
        name.capitalize()
    )
