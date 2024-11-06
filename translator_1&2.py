import requests
from bs4 import BeautifulSoup


def translation_direction():
    while True:
        lang = input('Type "en" if you want to translate from French into '
                     'English, or "fr" if you want to translate from English '
                     'into French:\n').strip()
        if lang in ['en', 'fr']:
            return lang
        else:
            print(f'{lang} is not "en" or "fr". Try again!')


def create_url():
    lang = translation_direction()
    word = input('Type the word you want to translate:\n').strip()
    print(f'You chose "{lang}" as a language to translate "{word}".')

    direction = 'french-english' if lang == 'en' else 'english-french'
    return f'https://context.reverso.net/translation/{direction}/{word}'


def fetch_translations(url):
    headers = {'User-Agent':
                   'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
    response = requests.get(url, headers=headers)
    print(f'{response.status_code} OK')
    print('Translations')

    soup = BeautifulSoup(response.content, 'html.parser')

    translations = soup.find_all(class_='display-term')
    translation_list = [word.text for word in translations]

    sentences = soup.find(id="examples-content").find_all(class_="text")
    sentences_list = [sentence.text.strip() for sentence in sentences]

    print(translation_list)
    print(sentences_list)


def main():
    url = create_url()
    if url:
        fetch_translations(url)


if __name__ == "__main__":
    main()