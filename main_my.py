from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import json

driver = webdriver.Firefox()  # Или используйте другой драйвер, например, Chrome

# Заходим на сайт
driver.get("https://pegas.bsu.edu.ru/mod/quiz/view.php?id=1666675")

# Добавляем cookies
driver.add_cookie({'name': 'MoodleSession', 'value': 'j4ehlduh8l8tf4tnb3316f1e5p'})

# Находим кнопку и кликаем по ней
button = driver.find_element_by_id("single_button65a587bb5919d18")
button.click()

# Загружаем предыдущие ответы из файла JSON, если он существует
try:
    with open('answers.json', 'r') as f:
        previous_answers = json.load(f)
except FileNotFoundError:
    previous_answers = {}

# Находим все вопросы
questions = driver.find_elements_by_class_name("que")

for question in questions:
    # Получаем ID вопроса
    question_id = question.get_attribute("id")
    
    # Находим все варианты ответа в вопросе
    answers = question.find_elements_by_xpath(".//input[@type='radio']")
    
    # Если на этот вопрос уже был дан верный ответ, выбираем его
    if question_id in previous_answers and previous_answers[question_id] in [answer.get_attribute("value") for answer in answers]:
        correct_answer = [answer for answer in answers if answer.get_attribute("value") == previous_answers[question_id]][0]
        correct_answer.click()
    else:
        # Иначе выбираем случайный вариант ответа
        chosen_answer = random.choice(answers)
        chosen_answer.click()
        
        # Сохраняем выбранный вариант ответа
        previous_answers[question_id] = chosen_answer.get_attribute("value")

# Сохраняем ответы в файл JSON
with open('answers.json', 'w') as f:
    json.dump(previous_answers, f)

# Закрываем браузер после использования
# driver.close()
