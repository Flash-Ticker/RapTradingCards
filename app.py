from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_mysqldb import MySQL
from datetime import datetime
import os
import uuid

from templates.logic.dice_logic import Dice, DiceGame

# App Initialisierung
app = Flask(__name__, template_folder='templates')

# Secret Key setzen (wichtig für Sessions)
app.secret_key = 'your_secret_key_here'

# MySQL Konfiguration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tradingcards'

mysql = MySQL(app)

class GameSession:
    def __init__(self):
        self.games = {}

    def create_game(self, player_id, selected_cards):
        game_id = str(uuid.uuid4())
        self.games[game_id] = {
            'player_id': player_id,
            'selected_cards': selected_cards,
            'opponent_cards': [],
            'state': 'playing'
        }
        return game_id

    def get_game(self, game_id):
        return self.games.get(game_id)

game_manager = GameSession()
dice_game = DiceGame()

class LobbyManager:
    def __init__(self):
        self.lobbies = {}

    def create_lobby(self, player_id, selected_cards):
        date_str = datetime.now().strftime('%d%m%y')
        lobby_count = len(self.lobbies) + 1
        lobby_id = f"{date_str}-{lobby_count}"

        self.lobbies[lobby_id] = {
            'id': lobby_id,
            'player_id': player_id,
            'selected_cards': selected_cards,
            'opponent_cards': [],
            'state': 'active',
            'created_at': datetime.now()
        }
        return lobby_id

    def get_lobby(self, lobby_id):
        return self.lobbies.get(lobby_id)

lobby_manager = LobbyManager()

# -------- Basis-Routen --------
@app.route('/index')
def index():
    """Hauptseite: Zeigt alle Karten an"""
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM rapcards')
        rapcards = cur.fetchall()
        cur.close()
        return render_template('index.html', rapcards=rapcards)
    except Exception as e:
        print(f'Datenbankfehler: {e}')
        return jsonify({'error': 'Datenbankfehler'}), 500

@app.route('/cards', methods=['GET'])
def cards():
    """Kartenübersicht mit Suchfunktion"""
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM rapcards')
        columns = [col[0] for col in cur.description]
        cards = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return render_template('cards.html', cards=cards)
    except Exception as e:
        print(f'Datenbankfehler: {e}')
        return jsonify({'error': str(e)}), 500

# -------- API-Routen --------
@app.route('/api/items/cards', methods=['GET'])
def get_cards_api():
    """API-Endpunkt für Kartendaten"""
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM rapcards')
        cards = cur.fetchall()
        cur.close()
        return jsonify({'cards': cards}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    """Neue Karte hinzufügen"""
    if request.method == 'POST':
        try:
            card_data = {
                'artist_name': request.form['artist_name'],
                'title': request.form['title'],
                'lifepoints': request.form.get('lifepoints', 100),
                'style': request.form['style'],
                'flow': request.form['flow'],
                'lyric': request.form['lyric'],
                'beat': request.form['beat'],
                'video': request.form['video'],
                'serial_number': request.form['serial_number'],
                'release_date': request.form['release_date'],
                'img': request.form['img'],
                'songurl': request.form['songurl']
            }

            cur = mysql.connection.cursor()
            cur.execute('''
                INSERT INTO rapcards (artistname, title, lifepoints, style, flow, lyric, 
                beat, video, seriennummer, veroeffentlichung, img, songurl) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', tuple(card_data.values()))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('index'))
        except Exception as e:
            print(f'Fehler beim Hinzufügen: {e}')
            return jsonify({'error': 'Fehler beim Hinzufügen'}), 500
    return render_template('add_card.html')

# -------- Logic-Routen --------
@app.route('/roll-dice', methods=['GET', 'POST'])
def roll_dice():
    """Würfelt eine Zahl für Bot oder Spieler."""
    if request.method == 'POST':
        if request.json.get('role') == 'bot':
            result = dice_game.bot_roll_dice()
            return jsonify({'dice_result': result, 'message': 'Bot hat gewürfelt!'})
        elif request.json.get('role') == 'player':
            result = dice_game.player_roll_dice()
            return jsonify({'dice_result': result, 'message': 'Spieler hat gewürfelt!'})
    else:
        dice = Dice()  # Standard 6-seitiger Würfel
        result = dice.roll()
        return jsonify({'dice_result': result})

@app.route('/determine-first-turn', methods=['GET'])
def determine_first_turn():
    """Entscheidet, wer das Spiel beginnt."""
    message = dice_game.determine_first_turn()
    return jsonify({'message': message})

# -------- Spiel-Routen --------
@app.route('/games')
def games():
    """Spiele-Übersichtsseite"""
    return render_template('games.html')

@app.route('/game-selection', methods=['GET', 'POST'])
def game_selection():
    """Karten auswählen und Lobby erstellen"""
    try:
        if request.method == 'POST':
            selected_cards = request.form.get('selected_cards', '').split(',')
            if len(selected_cards) != 5:
                print("Fehler: Es wurden nicht genau 5 Karten ausgewählt.")
                return redirect(url_for('game_selection'))

            if 'player_id' not in session:
                session['player_id'] = str(uuid.uuid4())

            # Lobby erstellen
            lobby_id = lobby_manager.create_lobby(session['player_id'], selected_cards)
            session['lobby_id'] = lobby_id

            # Debugging-Ausgabe
            print(f"DEBUG: Lobby erstellt! Lobby ID: {lobby_id}")
            print(f"DEBUG: Ausgewählte Karten: {selected_cards}")

            # Weiterleitung zur game-field-Route
            return redirect(url_for('game_field', lobby_id=lobby_id))

        # Karten für die Auswahl anzeigen
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, artistname, title, img FROM rapcards ORDER BY RAND() LIMIT 10')
        random_cards = [dict(zip(['id', 'artist', 'title', 'image'], row)) for row in cur.fetchall()]
        cur.close()
        return render_template('game-selection.html', random_cards=random_cards)
    except Exception as e:
        print(f'Fehler in game_selection: {e}')
        return jsonify({'error': str(e)}), 500


@app.route('/game-field/<lobby_id>')
def game_field(lobby_id):
    """Spielfeld anzeigen mit ausgewählten Karten"""
    try:
        lobby = lobby_manager.get_lobby(lobby_id)
        if not lobby:
            return redirect(url_for('game_selection'))

        # Spieler-Karten aus der Lobby abrufen
        selected_cards = lobby['selected_cards']

        cur = mysql.connection.cursor()
        placeholders = ','.join(['%s'] * len(selected_cards))
        query = f"SELECT id, artistname, title, img FROM rapcards WHERE id IN ({placeholders})"
        cur.execute(query, tuple(selected_cards))
        player_cards = [dict(zip(['id', 'artist', 'title', 'image'], row)) for row in cur.fetchall()]
        cur.close()

        # Platzhalter für Bot-Karten (zufällig auswählen)
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, artistname, title, img FROM rapcards ORDER BY RAND() LIMIT 5")
        bot_cards = [dict(zip(['id', 'artist', 'title', 'image'], row)) for row in cur.fetchall()]
        cur.close()

        return render_template('game-field.html', 
                               player_cards=player_cards, 
                               bot_cards=bot_cards, 
                               lobby_id=lobby_id)
    except Exception as e:
        print(f'Fehler in game_field: {e}')
        return redirect(url_for('game_selection'))


if __name__ == '__main__':
    app.run(debug=True)
