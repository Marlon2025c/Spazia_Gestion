import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)

# Configuration de la clé secrète et de la session
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
def rechercher_utilisateurs(pseudo_utilisateurs, mot_de_passe):
    utilisateur = [
        {"pseudo": "Marlon", "mdp": "1234"},
        {"pseudo": "Akina", "mdp": "123456"},
        {"pseudo": "ADMIN", "mdp": "MW"}
    ]
    for utilisateur in utilisateur:
        if utilisateur['pseudo'] == pseudo_utilisateurs and utilisateur['mdp'] == mot_de_passe:
            return utilisateur
    return None    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        pseudo = request.form['pseudo']
        mdp = request.form['mdp']
        utilisateur = rechercher_utilisateurs(pseudo, mdp)
        if utilisateur is not None:
    
            session['pseudo'] = utilisateur['pseudo']
            print(session)
            return redirect(url_for('home'))
        else:
            return redirect(request.url)
    else:
        if 'pseudo' in session:
            return redirect(url_for('home'))
        return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/gestion_compte')
def gestion_compte():
    return render_template('gestion_compte.html')

@app.route('/logout')
def logout():
    session.pop('pseudo', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
