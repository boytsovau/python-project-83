from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os
from dotenv import load_dotenv
from validators import url as validate_url

app = Flask(__name__)
app.secret_key = 'supersecretkey'

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def connect_db():
    return psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def handle_urls():
    if request.method == 'GET':
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls ORDER BY id DESC")
        urls = cur.fetchall()
        conn.close()
        return render_template('urls.html', urls=urls)
    elif request.method == 'POST':
        url = request.form['url']

        if len(url) > 255:
            flash('URL не должен превышать 255 символов', 'error')
            return redirect(url_for('handle_urls'))

        if not validate_url(url):
            flash('Введенный URL недействителен', 'error')
            return redirect(url_for('handle_urls'))

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
        conn.commit()
        conn.close()

        flash('URL успешно добавлен', 'success')
        return redirect(url_for('handle_urls'))


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
    url = cur.fetchone()

    cur.execute("SELECT * FROM checks WHERE url_id = %s ORDER BY id DESC", (url_id,))
    checks = cur.fetchall()

    conn.close()

    return render_template('url.html', url=url, checks=checks)


if __name__ == '__main__':
    app.run(debug=True)
