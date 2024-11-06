import requests
from bs4 import BeautifulSoup


def translation_direction():
    languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
                 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian',
                 'Russian', 'Turkish']

    numbered_languages = {
        i: language for i, language in enumerate(languages, start=1)}


    print('Hello, welcome to the translator. Translator supports:')
    for key in numbered_languages:
        print(str(key) + '.', numbered_languages[key])

    while True:
        sel_source = input('Type the number of your language:\n').strip()
        if sel_source.isdigit() and int(sel_source) in numbered_languages:
            sel_target = input(
                'Type the number of language you want to translate to:\n')
            if sel_target.isdigit() and int(sel_target) in numbered_languages:
                return (numbered_languages[int(sel_source)],
                        numbered_languages[int(sel_target)])
            else:
                print(f'{sel_target} is not accepted, '
                      f'it must be a digit from 1 to 13. Try again!')
        else:
            print(f'{sel_source} is not accepted, '
                  f'it must be a digit from 1 to 13. Try again!')


def create_url():
    trans = translation_direction()
    trans_direction = f'{trans[0].lower()}-{trans[1].lower()}'
    word = input('Type the word you want to translate:\n').strip()

    return f'https://context.reverso.net/translation/{trans_direction}/{word}', trans


def fetch_translations(url, trans):
    headers = {'User-Agent':
            'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    translations = soup.find_all(class_='display-term')
    translation_list = [word.text for word in translations]

    sentences = soup.find(id="examples-content").find_all(class_="text")
    sentences_list = [sentence.text.strip() for sentence in sentences]

    print(f'\n{trans[1]} Translations:')
    print(*translation_list[:5], sep='\n')
    print(f'\n{trans[1]} Examples:')

    for i in range(0, 10, 2):
        print(f'{sentences_list[i]}\n{sentences_list[i + 1]}\n')

def main():
    url, trans = create_url()
    if url:
        fetch_translations(url, trans)


if __name__ == "__main__":
    main()