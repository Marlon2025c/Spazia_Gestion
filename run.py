import os
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import json
import os

app = Flask(__name__)

# Configuration de la clé secrète et de la session
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def rechercher_utilisateurs(pseudo_utilisateurs, mot_de_passe):
    utilisateurs = [
        {"pseudo": "Marlon", "mdp": "1234"},
        {"pseudo": "Akina", "mdp": "123456"}
    ]
    for utilisateur in utilisateurs:
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
    if 'pseudo' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('index'))
DATABASE_FOLDER = 'database'
DEPENSES_FILE = os.path.join(DATABASE_FOLDER, 'depenses_du_mois.json')
ENTREES_FILE = os.path.join(DATABASE_FOLDER, 'entrees_du_mois.json')

# Fonction pour sauvegarder les données dans un fichier JSON
def save_data(data, filename):
    # Créer le dossier s'il n'existe pas
    os.makedirs(DATABASE_FOLDER, exist_ok=True)
    
    # Charger les données existantes
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    
    # Ajouter les nouvelles données
    existing_data.append(data)
    
    # Sauvegarder les données mises à jour
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

@app.route('/gestion_compte', methods=['GET', 'POST'])
def gestion_compte():
    if 'pseudo' in session:
        if request.method == 'POST':
            selectype = request.form.get('selectype')
            if selectype == '1':
                depense_date = request.form.get('depense_date')
                depense_amount = request.form.get('depense_amount')
                depense_type = request.form.get('depense_type')
                depense_description = request.form.get('depense_description')
                # Traiter les données de dépense ici
                print(f"Dépense: {depense_date}, {depense_amount}, {depense_type}, {depense_description}")
                # Sauvegarder les données dans le fichier des dépenses
                data = {
                    "date": depense_date,
                    "depenses": depense_amount,
                    "type": depense_type,
                    "description": depense_description,
                    "utilisateur": session['pseudo']
                }
                save_data(data, DEPENSES_FILE)
            elif selectype == '2':
                entrees_date = request.form.get('entrees_date')
                entrees_amount = request.form.get('entrees_amount')
                entrees_type = request.form.get('entrees_type')
                entrees_description = request.form.get('entrees_description')
                # Traiter les données d'entrées ici
                print(f"Entrées: {entrees_date}, {entrees_amount}, {entrees_type}, {entrees_description}")
                # Sauvegarder les données dans le fichier des entrées
                data = {
                    "date": entrees_date,
                    "depenses": entrees_amount,
                    "type": entrees_type,
                    "description": entrees_description,
                    "utilisateur": session['pseudo']
                }
                save_data(data, ENTREES_FILE)
            # Retourner une réponse après avoir traité les données du formulaire
            return redirect(url_for('gestion_compte'))
        else:
            return render_template('form.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'pseudo' in session:
        session.pop('pseudo', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    """ Timer(0, open_browser).start()  # Ouvrir le navigateur après 1 seconde """
    app.run(debug=True)