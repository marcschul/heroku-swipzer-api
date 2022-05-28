import psycopg2
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from urllib.parse import urlparse
import os
from init_db import init

app = Flask(__name__)
CORS(app)
load_dotenv('.env')
init()

#Heroku DB Test
url = urlparse(os.environ.get('DATABASE_URL'))
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)

def get_db_connection():
    conn = psycopg2.connect(db)
    return conn
#------------

def get_db_connection():
    conn = psycopg2.connect(host=os.getenv("PG_HOST"),
                            database=os.getenv("PG_DATABASE"),
                            user=os.getenv("PG_USER"),
                            password=os.getenv("PG_PASSWORD"),
                            port=os.getenv("PG_PORT"))
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM games;")
    games = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', games=games)

@app.route('/json',methods=['GET','POST'])
def json():
  if request.method == 'GET':
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM games;')
    games = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(games)
  
  if request.method == 'POST':
    data = request.json
    print(data)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM games;')
    games = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(games)

@app.route('/games',methods=['GET','POST', 'PUT'])
def games():
  if request.method == 'GET':
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM games WHERE id=(SELECT MAX(id) FROM games);')
    lastGame = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(lastGame[0])

  if request.method == 'POST':
    data = request.json
    print(data)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO games (player1, player2, current_player, game_over, message, board)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            ('Player1',
             'Player2',
             '1',
             'false',
             'SWIPERZ',
             '{{0, 0, 0, 0, 0, 0, 0} , {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}}')
            )
    conn.commit()
    cur.execute('SELECT * FROM games WHERE id=(SELECT MAX(id) FROM games);')
    lastGame = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(lastGame[0])

  if request.method == 'PUT':
    data = request.json
    currentPlayer = data['appState']['currentPlayer']
    gameOver = data['appState']['gameOver']
    message = data['appState']['message']
    board = data['gameState']['board']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM games;")
    games = cur.fetchall()
    cur.execute('UPDATE games SET current_player=(%s), game_over=(%s), message=(%s), board=(%s) WHERE id=(%s);', [currentPlayer, gameOver, message, board, len(games)])
    conn.commit()
    cur.execute('SELECT * FROM games WHERE id=(SELECT MAX(id) FROM games);')
    lastGame = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(lastGame[0])

if __name__ == "__main__":
  app.run(debug=True)