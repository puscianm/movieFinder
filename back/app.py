from flask import Flask, render_template, jsonify
import os
import psycopg2
from random import choice
import my_app  # Import your existing my_app.py

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT")
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_random_match')
def get_random_match():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT match_begin_time, host_name, guest_name FROM schedule')
    matches = cur.fetchall()
    cur.close()
    conn.close()
    
    if matches:
        random_match = choice(matches)
        return jsonify({
            'time': random_match[0].strftime('%Y-%m-%d %H:%M:%S'),
            'host': random_match[1],
            'guest': random_match[2]
        })
    else:
        return jsonify({'error': 'No matches found'})

if __name__ == '__main__':
    my_app.main()  # Run your existing main function to populate the database
    app.run(host='0.0.0.0', port=8000)
