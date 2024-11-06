import requests
from bs4 import BeautifulSoup


languages = {0: 'All', 1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish',
                 5: 'French', 6: 'Hebrew', 7: 'Japanese', 8: 'Dutch',
                 9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian',
                 13: 'Turkish'}

def translation_direction():
    print('Hello, welcome to the translator. Translator supports:')
    for key in range(1,len(languages)):
        print(str(key) + '.', languages[key])

    while True:
        sel_source = input('Type the number of your language:\n').strip()
        if sel_source.isdigit() and int(sel_source) in languages:
            sel_target = input("Type the number of a language you want to "
                               "translate to or '0' to translate to all "
                               "languages:\n").strip()
            if sel_target.isdigit() and int(sel_target) in languages:
                return (languages[int(sel_source)],
                        languages[int(sel_target)])
            else:
                print(f'{sel_target} is not accepted, '
                      f'it must be a digit from 0 to 13. Try again!')
        else:
            print(f'{sel_source} is not accepted, '
                  f'it must be a digit from 0 to 13. Try again!')


def create_url():
    trans = translation_direction()
    word = input('Type the word you want to translate:\n').strip()
    url_lst = []
    if trans[1] != 'All':
        trans_direction = f'{trans[0].lower()}-{trans[1].lower()}'
        url_lst.append(f'https://context.reverso.net/translation/'
        f'{trans_direction}/{word}')
    else:
        for i in range(1,len(languages)):
            if trans[0] == languages[i]:
                continue
            trans_direction = f'{trans[0].lower()}-{languages[i].lower()}'
            url_lst.append(f'https://context.reverso.net/translation/{
            trans_direction}/{word}')
    return url_lst, trans, word


def fetch_translations(url_lst, trans, word):
    with open(f'{word}.txt', 'w', encoding='utf-8') as f:
        headers = {'User-Agent':
                'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}

        tagged = False
        for i, url in enumerate(url_lst, start=1):
            if trans[0] == languages[i]:
                tagged = True
            key = i + 1 if tagged else i

            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.content, 'html.parser')

            translations = soup.find_all(class_='display-term')
            translation_list = [trans_word.text for trans_word in translations]

            sentences = soup.find(id="examples-content").find_all(class_="text")
            sentences_list = [sentence.text.strip() for sentence in sentences]

            if len(url_lst) == 1:
                key = next((k for k, v in languages.items() if v == trans[1]), None)

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
    url_lst, trans, word = create_url()
    if url_lst:
        fetch_translations(url_lst, trans, word)


if __name__ == "__main__":
    main()