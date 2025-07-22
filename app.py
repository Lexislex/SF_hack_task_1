from flask import Flask, render_template, request

app = Flask(__name__)

# Функция-обработчик (наш "скрипт")
def process_data(data):
    # Здесь может быть любая логика обработки
    processed = f"Вы ввели: {data['name']}. Длина имени: {len(data['name'])} символов."
    
    # Правильная проверка чекбокса
    if data.get('newsletter') == 'yes':
        processed += " Вы подписаны на рассылку."
    else:
        processed += " Вы НЕ подписаны на рассылку."
    return processed

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Получаем данные из формы
        form_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'newsletter': request.form.get('newsletter')  # будет 'yes' если отмечено, иначе None
        }
        # Отправляем данные в наш "скрипт" для обработки
        result = process_data(form_data)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)