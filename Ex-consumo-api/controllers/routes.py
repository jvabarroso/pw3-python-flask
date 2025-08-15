import urllib.request
from flask import render_template, request, url_for
import json



def init_app(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/frases', methods=['GET', 'POST'])
    def frases(id=None):

        if id:
            url = f'https://api.quotable.io/quotes/{id}'
        else:
            url = 'https://api.quotable.io/random'

        response = urllib.request.urlopen(url)
        apiData = response.read()
        frasesList = json.loads(apiData)

        if id:
            frase = []
            for f in frasesList:
                if f['id'] == id:
                    f = frase
                    break
        if frase:
            return render_template('filosofia.html', frase=frase)
        else:
            f"{id} não encontrado"
