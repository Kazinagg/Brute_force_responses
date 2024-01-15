from bs4 import BeautifulSoup
import requests
import json

url = 'https://pegas.bsu.edu.ru/mod/quiz/attempt.php?attempt=5102183&page=0'



cookies = dict(_ym_uid='16475500421009571758', _ym_d='1705315801', _ym_isad='1', MoodleSession='82objt0il20mfdhef5noo6m1ln')

page = requests.get(url, cookies=cookies)
src = page.text

html = BeautifulSoup(src, "lxml")

quest = html.findAll('div', class_='qtext')
ans = html.findAll('div', class_='answer')

all_questions = {}
all_ans = {}

for answer in ans:
    names = answer.find('div').find('input')
    names = names.get('name')
    id_ans = names.split(':')
    id_ans = id_ans[1].split('_')
    all_ans[id_ans[0]] = answer.text



for question in quest:
    quest_names = question.parent.find('input')
    quest_names = quest_names.get('name')
    id_quest = quest_names.split(':')
    id_quest = id_quest[1].split('_')
    id_quest = id_quest[0]
    if(f'{id_quest}' in all_ans):
        all_questions[id_quest] = [f'{question.text}', f"{all_ans[f'{id_quest}']}"]
    else:
        all_questions[id_quest] = [f'{question.text}', f'None']




with open('result.json', 'w') as file:
    json.dump(all_questions, file, indent=4, ensure_ascii=False)

