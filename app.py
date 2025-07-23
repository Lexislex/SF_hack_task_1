from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
# app.config['APPLICATION_ROOT'] = '/hackathon'

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
            additional_results.append(f"{FIELD_TYPES[field_name]['label']}: {value}")
    
    if len(additional_results) == 1:
        additional_results.append("Нет дополнительных полей")
    
    return "<br>".join(result + required_results + additional_results)

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