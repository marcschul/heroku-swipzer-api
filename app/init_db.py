import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="swiperz_db",
        user='swiperz',
        password='swiperz')

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS games;')
cur.execute('CREATE TABLE games (id serial PRIMARY KEY,'
                                 'player1 varchar (150) NOT NULL,'
                                 'player2 varchar (150) NOT NULL,'
                                 'current_player varchar (150) NOT NULL,'
                                 'game_over varchar (150) NOT NULL DEFAULT FALSE,'
                                 'message varchar (150),'
                                 'board int[][],'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table
cur.execute('INSERT INTO games (player1, player2, current_player, game_over, board)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('Player1',
             'Player2',
             '1',
             'true',
             '{{0, 1, 1, 1, 0, 0, 1} , {0, 1, 1, 1, 0, 0, 1}, {0, 1, 1, 1, 0, 0, 1}, {0, 1, 1, 1, 0, 0, 1}, {0, 1, 1, 1, 0, 0, 1}, {0, 1, 1, 1, 0, 0, 1}, {0, 1, 1, 1, 0, 0, 1}}')
            )

cur.execute('INSERT INTO games (player1, player2, current_player, game_over, board)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('Player1',
             'Player2',
             '2',
             'false',
             '{{0, 0, 0, 0, 0, 0, 0} , {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}}')
            )

cur.execute('INSERT INTO games (player1, player2, current_player, game_over, board)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('Player1',
             'Player2',
             '2',
             'false',
             '{{1, 0, 0, 0, 0, 0, 0} , {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0}}')
            )

conn.commit()

cur.close()
conn.close()