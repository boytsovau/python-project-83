from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os
from dotenv import load_dotenv
from validators import url as validate_url


app = Flask(__name__)
app.secret_key = 'supersecretkey'

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_url', methods=['POST'])
def add_url():
    url = request.form['url']

    if len(url) > 255:
        flash('URL не должен превышать 255 символов', 'error')
        return redirect(url_for('index'))

    if not validate_url(url):
        flash('Введенный URL недействителен', 'error')
        return redirect(url_for('index'))

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
    conn.commit()
    conn.close()

    flash('URL успешно добавлен', 'success')
    return redirect(url_for('index'))


@app.route('/urls')
def show_urls():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls ORDER BY id DESC")
    urls = cur.fetchall()
    conn.close()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
    url = cur.fetchone()
    conn.close()
    return render_template('url.html', url=url)
