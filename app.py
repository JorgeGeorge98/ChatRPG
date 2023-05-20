from os import environ
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse, unquote
import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_API_KEY')

story_begun = False
previous_response = ""

@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")

@app.route('/fantasia', methods=("GET",))
def fantasia():
    return render_template("fantasia.html")

@app.route('/apiCall', methods=("POST",))
def apiCall():
    global story_begun
    global previous_response

    userInput = request.form["userInput"]
    response = openai.Completion.create(
        model="text-davinci-003",
        max_tokens=3000,
        prompt=generate_prompt(userInput, story_begun, previous_response),
        temperature=1,
    )
    previous_response = response.choices[0].text
    imgUrl = openai.Image.create(
        prompt=response.choices[0].text,
        n=1,
        size="256x256"
    )
    if not story_begun:
        story_begun = True
    
    decoded_url = None
    if imgUrl['data'][0]['url']:
        decoded_url = custom_unquote(imgUrl['data'][0]['url'])
    
    return jsonify({"result": response.choices[0].text, "imgUrl": decoded_url})

def generate_prompt(userInput, story_begun, previous_response = ""):

    if story_begun:
        return """Genera la continuacion de la historia de fantasia de una forma coherente a partir de la respuesta del usuario, maximo un parrafo que termine de forma abierta para que el usuario pueda seguir la historia

        Historia: {}
        Respuesta del usuario: {}
        Continuacion de la historia:""".format(previous_response ,userInput.capitalize())
    else:
        return """Comienza una historia de fantasia con el nombre que se introduce

        Nombre: Pepe
        Historia: Pepe caminaba por un bosque encantado cuando encontro a un ogro llamado Alexander, que hace pepe?
        Nombre: Jose
        Historia: Jose se a despertado en una mazmorra encadenado en un traje de cuero BDSM, a Jose le gusta, que hace jose?
        Nombre: {}
        Historia:""".format(userInput.capitalize())
    
def custom_unquote(url):
    parsed_url = urlparse(url)
    query_params = parse_qsl(parsed_url.query)
    decoded_query_params = []

    for key, value in query_params:
        if key == 'sig':
            value = value.replace('+', '%2B')
            value = unquote(value)
        decoded_query_params.append((key, value))

    decoded_query_string = urlencode(decoded_query_params)
    decoded_url = urlunparse(parsed_url._replace(query=decoded_query_string))
    return decoded_url
