from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Обязательные поля с значениями по умолчанию
REQUIRED_FIELDS = {
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

# Доступные типы полей для добавления
FIELD_TYPES = {
    'text': {'type': 'text', 'label': 'Текстовое поле', 'default': 'Значение по умолчанию'},
    'email': {'type': 'email', 'label': 'Email', 'default': 'example@mail.com'},
    'number': {'type': 'number', 'label': 'Число', 'default': 0},
    'agreement': {'type': 'checkbox', 'label': 'Согласие', 'value': 'yes', 'default': True},
    'birthdate': {'type': 'date', 'label': 'Дата рождения', 'default': '2000-01-01'},
    'gender': {'type': 'select', 'label': 'Пол', 
               'options': ['Мужской', 'Женский'], 'default': 'Мужской'}
}

def process_data(form_data):
    required_results = ["<strong>Обязательные поля:</strong>"]
    additional_results = ["<strong>Дополнительные поля:</strong>"]
    recomendations = ["<strong>Рекомендации:</strong>"]

    for field_name, value in form_data.items():
        if field_name in REQUIRED_FIELDS:
            required_results.append(f"{REQUIRED_FIELDS[field_name]['label']}: {value}")
        elif field_name not in ['add_field', 'field_type', 'field_count']:
            additional_results.append(f"{FIELD_TYPES[field_name]['label']}: {value}")
    
    if len(additional_results) == 1:
        # additional_results.append("Нет дополнительных полей")
        additional_results.clear()

    # Тут должен быть вызов функции предсказания и рекомендаций
    # print(form_data.to_dict())
    
    return "<br>".join(required_results + additional_results + recomendations)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add_field' in request.form:
            # Обработка добавления нового поля (AJAX запрос)
            field_type = request.form.get('field_type')
            field_key = field_type  # Используем ключ из FIELD_TYPES как имя поля
            
            field_config = FIELD_TYPES.get(field_type, FIELD_TYPES['gender'])
            return jsonify({
                'html': render_template('_field.html', 
                                     field_id=field_key,  # Используем ключ как ID
                                     field_name=field_key,  # Используем ключ как name
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