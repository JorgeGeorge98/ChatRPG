1: Crea nueva carpeta y dentro de ella ejecuta : git clone https://github.com/JorgeGeorge98/ProyectoFinal.git
2: Navegar a la respectiva rama
3: Ejecutar
```bash
python -m venv venv
. venv/bin/activate -por si acaso
pip install -r requirements.txt
cp .env.example .env -por si acaso
```

4: Crear fichero '.env' en la raiz del proyecto e incluir esto dentro:
```bash
FLASK_APP=app
FLASK_ENV=development

# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.
OPENAI_API_KEY=
```
python -m flask run
