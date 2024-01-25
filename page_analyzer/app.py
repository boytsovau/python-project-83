import requests
import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
)
from datetime import datetime
from page_analyzer.validator import (
    validate_url,
    collect_page_data,
    get_normalized_url
)
from page_analyzer.database import (
    add_url_record,
    add_check_record,
    get_url_by_name,
    get_url_by_id,
    get_checks_url_by_id,
    urls_with_last_check_info
)


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url_fields_dct = request.form.to_dict()
    url_fields_dct['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    normalize_url = get_normalized_url(url_fields_dct['url'])

    url_validation_errors = validate_url(normalize_url)

    if url_validation_errors:
        for error in url_validation_errors:
            flash(error, 'alert-danger')
        return render_template(
            'index.html',
            url=url_fields_dct['url'],
            errors=get_flashed_messages(with_categories=True)
        ), 422

    url_found = get_url_by_name(normalize_url)
    page_already_exists_error = 'Страница уже существует'
    if url_found:
        flash(page_already_exists_error, 'alert-primary')
        id = url_found['id']
        return redirect(url_for('get_one_url', id=id))

    url_fields_dct['url'] = normalize_url
    new_url_id = add_url_record(url_fields_dct)
    flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('get_one_url', id=new_url_id))


@app.get('/urls')
def get_all_urls():
    all_urls = urls_with_last_check_info()
    return render_template('urls.html', urls=all_urls)


@app.get('/urls/<id>')
def get_one_url(id):
    url = get_url_by_id(id)
    checks = get_checks_url_by_id(id)
    return render_template('url.html', url=url, checks=checks)


@app.post('/urls/<id>/checks')
def add_check(id):
    url_record = get_url_by_id(id)
    url = url_record['name']
    try:
        http_response = requests.get(url)
        http_response.raise_for_status()
        check_record = collect_page_data(id, http_response)
        add_check_record(check_record)
        flash('Страница успешно проверена', 'alert-success')
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
    return redirect(url_for('get_one_url', id=id))

