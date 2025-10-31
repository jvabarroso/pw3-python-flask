import urllib.request
import json
from flask import render_template, request, redirect, url_for, flash
import os
from models.database import db, Imagem
import uuid

def init_app(app):
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
                    'numOng': ong['phone_number'],
                    'email': ong['email']
                })
                
        except:
            previews = []

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
        
    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        imagem = Imagem.query.all()
        if request.method == 'POST':
            file = request.files['file']
            if not arquivos_permitidos(file.filename):
                flash('Tipo de arquivo não permitido.', 'danger')
                return redirect(request.url)
            
            filename = str(uuid.uuid4())
            
            img = Imagem(filename)
            db.session.add(img)
            db.session.commit()
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Arquivo enviado com sucesso!', 'success')
            return redirect(url_for('galeria'))
        return render_template('galeria.html', imagem=imagem)
    
    FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])
    def arquivos_permitidos(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES
    