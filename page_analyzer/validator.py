import validators


def validate_url(url):
    errors = []
    if not url:
        errors.append("URL обязателен")
    elif not validators.url(url):
        errors.append('Некорректный URL')
    return errors
