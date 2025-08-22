import urllib.request
import json
from flask import render_template

def init_app(app):

    @app.route('/')
    def home():
        return ongs()

    @app.route('/ongs')
    def ongs():
            url = 'https://ongs-brasil.org/api/ongs'
            resp = urllib.request.urlopen(url, timeout=10)
            data = json.loads(resp.read())

            previews = []
            for ong in data.get('data', []):
                previews.append({
                    'id': ong['id'],
                    'nome': ong['name'],
                    'numOng': ong['phone_number'],
                    'email': ong['email']
                })

            return render_template('index.html', previews=previews)

    @app.route('/ongs/<id>')
    def ong_detail(id):
            url = f'https://ongs-brasil.org/api/ongs?id={id}'
            resp = urllib.request.urlopen(url)
            data = json.loads(resp.read())
            matches = data.get('data', [])
            
            if matches:
                ong = matches[0]
                detail = {
                    'nome': ong.get('name'),
                    'descricao': ong.get('description'),
                    'website': ong.get('website'),
                    'numOng': ong.get('phone_number'),
                    'email': ong.get('email'),
                }
            else:
                detail = {
                    'nome': 'Não encontrada',
                    'descricao': '',
                    'website': '',
                    'numOng': '',
                    'email': ''
                }

            return render_template('info.html', detail=detail)