import os
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse, unquote
import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]
#environ["OPENAI_API_KEY"]
#os.environ.get('OPENAI_API_KEY')

story_begun = False
previous_response = ""
clase_boton = ""

@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")

@app.route ('/guardar', methods=("POST",))
def guardar():
    global clase_boton
    data = request.get_json()
    clase_boton = data['clase']

@app.route('/fantasia', methods=("GET",))
def fantasia():
    return render_template("fantasia.html")

@app.route('/scifi', methods=("GET",))
def scifi():
    return render_template("scifi.html")

@app.route('/terror', methods=("GET",))
def terror():
    return render_template("terror.html")

@app.route('/historico', methods=("GET",))
def historico():
    return render_template("historico.html")

@app.route('/postapo', methods=("GET",))
def postapo():
    return render_template("postapo.html")

@app.route('/misterio', methods=("GET",))
def misterio():
    return render_template("misterio.html")


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
    global clase_boton
    if clase_boton == "fantasiaButton":
        if story_begun:
            return """Genera la continuacion de la historia de fantasia de una forma coherente a partir de la respuesta del usuario, maximo un parrafo que termine de forma abierta para que el usuario pueda seguir la historia

                Historia: {}
                Respuesta del usuario: {}
                Continuacion de la historia:""".format(previous_response ,userInput.capitalize())
        
        else:
            return """Comienza una historia de fantasia con el nombre que se introduce

            Nombre: Pepe
            Historia: Pepe caminaba por un bosque encantado cuando encontro a un ogro que le esperaba junto a un árbol, que hace Pepe?
            Nombre: Jose
            Historia: Jose se ha despertado en una mazmorra encadenado, no hay nadie cerca y apenas puede moverse, que hace jose?
            Nombre: {}
            Historia:""".format(userInput.capitalize())

    elif clase_boton == "terrorButton":
        if story_begun:
                return """Genera la continuación de la historia de terror de forma coherente a partir de la respuesta del usuario, 
                máximo un párrafo que termine de forma abierta para que el usuario pueda seguir la historia.

                Historia: {}
                Respuesta del usuario: {}
                Continuación de la historia:""".format(previous_response, userInput.capitalize())
        else:
                return """Comienza una historia de terror con el nombre que se introduce.

                Nombre: Pepe
                Historia: Pepe caminaba por un antiguo cementerio cuando escuchó un susurro siniestro, ¿qué hace Pepe?
                Nombre: Jose
                Historia: Jose se despertó en una mansión abandonada, rodeado de sombras y un ambiente escalofriante, ¿qué hace Jose?
                Nombre: {}
                Historia:""".format(userInput.capitalize())
        
    elif clase_boton == "scifiButton":
        if story_begun:
                return """Genera la continuación de la historia de ciencia ficción de forma coherente a partir de la respuesta del usuario, 
                máximo un párrafo que termine de forma abierta para que el usuario pueda seguir la historia.

                Historia: {}
                Respuesta del usuario: {}
                Continuación de la historia:""".format(previous_response, userInput.capitalize())
        else:
                return """Comienza una historia de ciencia ficción con el nombre que se introduce.

                Nombre: Pepe
                Historia: Pepe despertó en una nave espacial abandonada, rodeado de luces parpadeantes y una sensación de peligro inminente, ¿qué hace Pepe?
                Nombre: Jose
                Historia: Jose se encontró de repente en un mundo futurista lleno de androides y tecnología avanzada, ¿qué hace Jose?
                Nombre: {}
                Historia:""".format(userInput.capitalize())
            
    elif clase_boton == "historicoButton":
        if story_begun:
                return """Genera la continuación de la historia histórica de forma coherente a partir de la respuesta del usuario, 
                máximo un párrafo que termine de forma abierta para que el usuario pueda seguir la historia.
                Historia: {}
                Respuesta del usuario: {}
                Continuación de la historia:""".format(previous_response, userInput.capitalize())
        else:
                return """Comienza una historia histórica con el nombre que se introduce.
                Nombre: Pepe
                Historia: Pepe se encontraba en medio de una batalla épica en la antigua Roma, rodeado de soldados y el sonido de las espadas chocando, ¿qué hace Pepe?
                Nombre: Jose
                Historia: Jose viajó en el tiempo y se encontró en plena Revolución Francesa, en medio de la agitación de las calles de París, ¿qué hace Jose?
                Nombre: {}
                Historia:""".format(userInput.capitalize())
        
    elif clase_boton == "postapoButton":
        if story_begun:
                return """Genera la continuación de la historia post-apocalíptica de forma coherente a partir de la respuesta del usuario, 
                máximo un párrafo que termine de forma abierta para que el usuario pueda seguir la historia.
                Historia: {}
                Respuesta del usuario: {}
                Continuación de la historia:""".format(previous_response, userInput.capitalize())
        else:
                 return """Comienza una historia post-apocalíptica con el nombre que se introduce.
                Nombre: Pepe
                Historia: Pepe despertó en un mundo devastado por un cataclismo nuclear, rodeado de ruinas y desolación, ¿qué hace Pepe para sobrevivir?
                Nombre: Jose
                Historia: Jose se encontró en un futuro post-apocalíptico donde los recursos son escasos y las bandas de saqueadores dominan las calles, ¿cómo se defiende Jose en este peligroso mundo?
                Nombre: {}
                Historia:""".format(userInput.capitalize())
        
    elif clase_boton == "misterioButton":
                if story_begun:
                    return """Genera la continuación de la historia de misterio de forma coherente a partir de la respuesta del usuario, 
                    máximo un párrafo que termine de forma abierta para que el usuario pueda seguir la historia.
                    Historia: {}
                    Respuesta del usuario: {}
                    Continuación de la historia:""".format(previous_response, userInput.capitalize())
                else:
                     return """Comienza una historia de misterio con el nombre que se introduce.
                    Nombre: Pepe
                    Historia: Pepe se encontró con un sobre misterioso en la puerta de su casa, dentro había una fotografía antigua y una nota enigmática, ¿qué hace Pepe para descubrir el secreto oculto?
                    Nombre: Jose
                    Historia: Jose recibió una llamada anónima en la que le advirtieron sobre un peligro inminente, ahora debe seguir las pistas y descubrir quién está detrás de todo, ¿cómo se adentra Jose en este intrigante misterio?
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
