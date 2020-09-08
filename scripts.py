def get_biology(**kwargs):
    from bs4 import BeautifulSoup
    import requests as rq

    month = kwargs['month']
    year = kwargs['year']
    level = kwargs['level']
    version = kwargs['version']
    exercise = kwargs['exercise']

    url = f'https://biologhelp.pl/matura/matura-{month.lower()}-{year}-poziom-{level}-{version}/zadanie-{exercise}'
    r = rq.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    div_answers = soup.find('div', class_='field field--name-field-answer field--type-text-long field--label-above')
    text = div_answers.get_text()
    return text


def get_photo(url, name):
    import requests as rq
    r = rq.get(url)
    with open(name, 'wb') as photo:
        photo.write(r.content)


def get_weather(city='warszawa'):
    import requests as rq
    from bs4 import BeautifulSoup
    from PIL import Image
    import os

    r = rq.get(f'http://{city.lower()}.infometeo.pl/')
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find('img', id="icm60h-meteogram")
    src = tag['src']

    ph_name = 'weather.png'
    with open(ph_name, 'wb') as new:
        photo = rq.get(src).content
        new.write(photo)

    with open(ph_name, 'rb') as photo:
        img = Image.open(photo)
        img.show()

    os.remove(ph_name)
