from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import threading
from src.utils.config import WEB_HOST, WEB_PORT, DEBUG_MODE
from src.alerting.alert_manager import AlertManager

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_secure_random_secret'
alert_manager = AlertManager()

VALID_USER = 'admin'
VALID_PASSWORD = 'admin'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == VALID_USER and password == VALID_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        error = 'Identifiants incorrects. Veuillez réessayer.'
    return render_template('login.html', error=error)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/api/alerts')
def get_alerts():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    alerts = alert_manager.get_latest_alerts(limit=50)
    return jsonify(alerts)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def run_web_server():
    """Fonction pour lancer Flask dans un thread"""
    # Note: debug=False est requis pour exécuter Flask dans un thread sans erreur
    app.run(host=WEB_HOST, port=WEB_PORT, debug=False, use_reloader=False)
