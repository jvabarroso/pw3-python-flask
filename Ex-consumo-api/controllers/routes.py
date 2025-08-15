import urllib.request
from flask import render_template, request, url_for
import json



def init_app(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/frases', methods=['GET', 'POST'])
    @app.route('/frases/<int:id>', methods=['GET', 'POST'])
    def frases(id=None):
        try:
            url = 'https://api.quotable.io/random'
            response = urllib.request.urlopen(url)
            apiData = response.read()
            frasesList = json.loads(apiData)
            
            # Se id existir (ou seja, foi informado parâmetro)
            if id:
                frase = []
                for f in frasesList:
                    if f['id'] == id:
                        frase = f
                        break
                if frase:
                    return render_template('filosofia.html', frase=frase)
                else:
                    return f'Frase com a ID {id} não foi encontrada.'
            else:
                # Para a rota /frases sem ID, pegar apenas uma frase aleatória
                frase = {
                    'texto': frasesList.get('content', 'Frase não disponível'),
                    'autor': frasesList.get('author', 'Autor desconhecido')
                }
                return render_template('filosofia.html', frase=frase)
        except:
            # Em caso de erro, retornar uma frase padrão
            frase = {
                'texto': 'A sabedoria começa na admiração.',
                'autor': 'Sócrates'
            }
            return render_template('filosofia.html', frase=frase)
