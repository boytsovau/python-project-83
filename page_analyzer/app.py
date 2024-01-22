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
    get_check_url,
    get_normalized_url
)
from page_analyzer.database import (
    add_url_record,
    add_check_record,
    get_url_by_name,
    get_all_url_records,
    get_url_by_id,
    get_checks_url_by_id,
    get_last_check_url
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

    errors = validate_url(normalize_url)

    page_already_exists_error = 'Страница уже существует'
    invalid_url_error = 'Некорректный URL'
    required_url_error = 'URL обязателен'

    def render_error_template(template, flash_category):
        flash(error, flash_category)
        return render_template(
            template,
            url=url_fields_dct['url'],
            errors=get_flashed_messages(with_categories=True)
        ), 422

    for error in errors:
        if error == required_url_error:
            return render_error_template('index.html', 'alert-danger')

        if error == invalid_url_error:
            return render_error_template('index.html', 'alert-danger')

        if error == page_already_exists_error:
            url_record = get_url_by_name(normalize_url)
            if url_record:
                flash(page_already_exists_error, 'alert-primary')
                id = url_record['id']
                return redirect(url_for('get_one_url', id=id))

    url_fields_dct['url'] = normalize_url
    add_url_record(url_fields_dct)
    flash('Страница успешно добавлена', 'alert-success')
    url_record = get_url_by_name(normalize_url)
    id = url_record['id']
    return redirect(url_for('get_one_url', id=id))



@app.get('/urls')
def get_all_urls():
    all_urls = get_all_url_records()
    last_check = get_last_check_url()
    return render_template('urls.html', urls=all_urls, last_check=last_check)


@app.get('/urls/<id>')
def get_one_url(id):
    url = get_url_by_id(id)
    checks = get_checks_url_by_id(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html',
                           url=url,
                           messages=messages, checks=checks
                           )


@app.post('/urls/<id>/checks')
def add_check(id):
    url_record = get_url_by_id(id)
    url = url_record['name']
    try:
        http_response = requests.get(url)
        http_response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('get_one_url', id=id))
    else:
        check_record = get_check_url(id, http_response)
        add_check_record(check_record)
        flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('get_one_url', id=id))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
                           message='Страница не найдена!'
                           ), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                           message='Внутренняя проблема сервера.'
                           ), 500


if __name__ == "__main__":
    app.run(debug=True)
