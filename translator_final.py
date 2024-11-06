import sys
import requests
from bs4 import BeautifulSoup

languages = {0: 'All', 1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish',
             5: 'French', 6: 'Hebrew', 7: 'Japanese', 8: 'Dutch',
             9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian',
             13: 'Turkish'}

url_lst = []
trans_dir = []
file_name = ''


def translation_direction(source_language, target_language):
    if source_language.capitalize() in languages.values():
        trans_dir.append(source_language.capitalize())
    else:
        print(f"Sorry, the program doesn't support {source_language}")
        sys.exit(1)

    if target_language.capitalize() in languages.values():
        trans_dir.append(target_language.capitalize())
    else:
        print(f"Sorry, the program doesn't support {target_language}")
        sys.exit(1)


def create_url(word):
    global file_name;
    file_name = word
    if trans_dir[1] != 'All':
        trans_direction = f'{trans_dir[0].lower()}-{trans_dir[1].lower()}'
        url_lst.append(f'https://context.reverso.net/translation/'
                       f'{trans_direction}/{word}')
    else:
        for i in range(1, len(languages)):
            if trans_dir[0] == languages[i]:
                continue
            trans_direction = f'{trans_dir[0].lower()}-{languages[i].lower()}'
            url_lst.append(f'https://context.reverso.net/translation/{
            trans_direction}/{word}')


def fetch_translations(word):
    with open(f'{word}.txt', 'w', encoding='utf-8') as f:
        headers = {'User-Agent':
            'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
        tagged = False
        for i, url in enumerate(url_lst, start=1):
            if trans_dir[0] == languages[i]:
                tagged = True
            key = i + 1 if tagged else i
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.ConnectionError:
                print('Something wrong with your internet connection')
                sys.exit(1)
            soup = BeautifulSoup(response.content, 'html.parser')
            translations = soup.find_all(class_='display-term')
            translation_list = [trans_word.text for trans_word in translations]
            sentences = soup.find(id="examples-content").find_all(class_="text")
            sentences_list = [sentence.text.strip() for sentence in sentences]

            if len(url_lst) == 1:
                key = next((k for k, v in languages.items() if v == trans_dir[1]), None)

            try:
                translation_list[0]
            except IndexError:
                print(f"Sorry, unable to find {word}")
                sys.exit(1)

            output = [
                f'{languages[key]} Translations:',
                translation_list[0],
                f'\n{languages[key]} Examples:',
                f'{sentences_list[0]}:\n{sentences_list[1]}\n\n'
            ]

            for line in output:
                print(line)
                f.write(line + '\n')


def main():
    if len(sys.argv) != 4:
        print("3 arguments are required")
        sys.exit(1)

    source_language = sys.argv[1].strip()
    target_language = sys.argv[2].strip()
    word = sys.argv[3].strip()

    translation_direction(source_language, target_language)
    create_url(word)
    fetch_translations(word)


if __name__ == "__main__":
    main()