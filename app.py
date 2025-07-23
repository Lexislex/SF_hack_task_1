from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Доступные типы полей для добавления
FIELD_TYPES = {
    'text': {'type': 'text', 'label': 'Текстовое поле', 'default': '+79991234567'},
    'email': {'type': 'email', 'label': 'Email'},
    'number': {'type': 'number', 'label': 'Число'},
    'checkbox': {'type': 'checkbox', 'label': 'Чекбокс', 'value': 'yes'},
    'date': {'type': 'date', 'label': 'Дата'},
    'select': {'type': 'select', 'label': 'Выпадающий список', 
               'options': ['Вариант 1', 'Вариант 2', 'Вариант 3']}
}

# Обязательные поля с значениями по умолчанию
REQUIRED_FIELDS = {
    # 'first_name': {'type': 'text', 'label': 'Имя', 'required': True, 'default': 'Иван'},
    # 'last_name': {'type': 'text', 'label': 'Фамилия', 'required': True, 'default': 'Иванов'},
    # 'email': {'type': 'email', 'label': 'Email', 'required': True, 'default': 'example@mail.com'},
    # 'phone': {'type': 'text', 'label': 'Телефон', 'required': True, 'default': '+79991234567'},
    'sex': {'type': 'select', 'label': 'Пол', 'required': True, 
            'options': ['Муж.', 'Жен.'], 'default': 'Муж.'},
    'birth_date': {'type': 'date', 'label': 'Дата рождения', 'required': True, 'default': '2000-01-01'},
    'hemoglobin': {
        'type': 'number', 
        'label': 'Гемоглобин', 
        'default': 120,
        'unit': 'г/л',
        'required': True
    },
    'leukocytes': {
        'type': 'number',
        'label': 'Лейкоциты',
        'default': 6.5,
        'unit': '×10⁹/л',
        'required': True
    },
    'erythrocytes': {
        'type': 'number',
        'label': 'Эритроциты',
        'default': 4.5,
        'unit': '×10¹²/л',
        'required': True
    }
}

def process_data(form_data):
    result = ["<strong>Обязательные поля:</strong>"]
    required_results = []
    additional_results = ["<strong>Дополнительные поля:</strong>"]
    
    for field_name, value in form_data.items():
        if field_name in REQUIRED_FIELDS:
            required_results.append(f"{REQUIRED_FIELDS[field_name]['label']}: {value}")
        elif field_name not in ['add_field', 'field_type', 'field_count']:
            additional_results.append(f"{field_name}: {value}")
    
    if len(additional_results) == 1:
        additional_results.append("Нет дополнительных полей")
    
    return "<br>".join(result + required_results + additional_results)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add_field' in request.form:
            # Обработка добавления нового поля (AJAX запрос)
            field_type = request.form.get('field_type')
            field_count = int(request.form.get('field_count', 0)) + 1
            field_id = f"custom_field_{field_count}"
            
            field_config = FIELD_TYPES.get(field_type, FIELD_TYPES['text'])
            return jsonify({
                'html': render_template('_field.html', 
                                     field_id=field_id,
                                     field_config=field_config)
            })
        elif 'new_form' in request.form:
            # Показать новую форму
            return render_template('index.html', 
                                field_types=FIELD_TYPES,
                                required_fields=REQUIRED_FIELDS,
                                result=None,
                                form_submitted=False)
        else:
            # Обработка основной формы
            result = process_data(request.form)
            return render_template('index.html', 
                                field_types=FIELD_TYPES,
                                required_fields=REQUIRED_FIELDS,
                                result=result,
                                form_submitted=True)
    
    # Первый заход - показать форму с данными по умолчанию
    return render_template('index.html', 
                         field_types=FIELD_TYPES,
                         required_fields=REQUIRED_FIELDS,
                         result=None,
                         form_submitted=False)

if __name__ == '__main__':
    app.run(debug=True)