import urllib.request
import json
from flask import render_template

def init_app(app):

    @app.route('/')
    def home():
        return ongs()

    @app.route('/ongs')
    def ongs():
        try:
            url = 'https://ongs-brasil.org/api/ongs'
            resp = urllib.request.urlopen(url, timeout=10)
            data = json.loads(resp.read())

            previews = []
            for ong in data.get('data', []):
                previews.append({
                    'id': ong['id'],
                    'nome': ong['name'],
                    'cidade': ong.get('city', ''),
                    'estado': ong.get('state', '')
                })

            return render_template('index.html', previews=previews)
            
        except Exception as e:
            # Se falhar, usar dados de exemplo
            previews = [
                {'id': 1, 'nome': 'ONG Exemplo 1', 'cidade': 'São Paulo', 'estado': 'SP'},
                {'id': 2, 'nome': 'ONG Exemplo 2', 'cidade': 'Rio de Janeiro', 'estado': 'RJ'},
                {'id': 3, 'nome': 'ONG Exemplo 3', 'cidade': 'Belo Horizonte', 'estado': 'MG'}
            ]
            return render_template('index.html', previews=previews)

    @app.route('/ongs/<id>')
    def ong_detail(id):
        try:
            url = f'https://ongs-brasil.org/api/ongs?id={id}'
            resp = urllib.request.urlopen(url, timeout=10)
            data = json.loads(resp.read())
            matches = data.get('data', [])
            
            if matches:
                ong = matches[0]
                detail = {
                    'nome': ong.get('name'),
                    'descricao': ong.get('description'),
                    'website': ong.get('website'),
                    'cidade': ong.get('city'),
                    'estado': ong.get('state')
                }
            else:
                detail = {
                    'nome': 'Não encontrada',
                    'descricao': '',
                    'website': '',
                    'cidade': '',
                    'estado': ''
                }

            return render_template('info.html', detail=detail)
            
        except Exception as e:
            # Se falhar, usar dados de exemplo
            detail = {
                'nome': 'ONG de Exemplo',
                'descricao': 'Esta é uma ONG de exemplo para demonstração.',
                'website': 'https://exemplo.org',
                'cidade': 'São Paulo',
                'estado': 'SP'
            }
            return render_template('info.html', detail=detail)
