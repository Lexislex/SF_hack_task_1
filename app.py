from flask import Flask, render_template, request, jsonify
from predict import predict

app = Flask(__name__)

# Обязательные поля с значениями по умолчанию
REQUIRED_FIELDS = {

    'gender': {
        'type': 'select',
        'label': 'Пол',
        'required': True, 
        'options': ['Мужской', 'Женский'],
        'default': 'Мужской',
        'tooltip': 'Пол пациента'
    },
    'birth_date': {
        'type': 'date',
        'label': 'Дата рождения',
        'required': True,
        'default': '2000-01-01',
        'tooltip': 'Дата рождения'    
    },
    'labstudy_date': {
        'type': 'date',
        'label': 'Дата проведения исследования',
        'required': True,
        'default': '2025-07-21',
        'tooltip': 'Дата забора материала'
    },

    'rbc': {
        'type': 'number',
        'label': 'Эритроциты',
        'default': 4.5,
        'unit': '×10¹²/л',
        'required': True,
        'tooltip': 'Норма: 3,8-5,8 × 10¹²/л'
    },
    'hgb': {
        'type': 'number', 
        'label': 'Гемоглобин', 
        'default': 120,
        'unit': 'г/л',
        'required': True,
        'tooltip': 'Норма: 120-140 г/л'
    },
    'hct': {
        'type': 'number', 
        'label': 'Гематокрит', 
        'default': 35,
        'unit': '%',
        'required': True,
        'tooltip': 'Норма: 39-49 %'
    },
    'cp': {
        'type': 'number', 
        'label': 'Цветовой показатель', 
        'default': 0.9,
        'unit': '',
        'required': True,
        'tooltip': 'Норма: 0,85-1'
    },
    'soe': {
        'type': 'number',
        'label': 'СОЭ',
        'default': 7,
        'unit': 'мм/ч',
        'required': True,
        'tooltip': 'Норма: 2-10 мм/ч'
    },

    'wbc': {
        'type': 'number',
        'label': 'Лейкоциты',
        'default': 6.5,
        'unit': '×10⁹/л',
        'required': True,
        'tooltip': 'Норма: 4-9 × 10⁹/л'
    },

    'plt': {
        'type': 'number',
        'label': 'Тромбоциты',
        'default': 200,
        'unit': '×10⁹/л',
        'required': True,
        'tooltip': 'Норма: 180-320 × 10⁹/л'
    }
    
}

FIELD_TYPES = {
    
    'pregnancy': {
        'type': 'number',
        'label': 'Срок беременности',
        'unit': 'нед.',
        'default': 16
    },

    'mcv': {'type': 'number', 'label': 'MCV', 'unit': 'фл', 'default': 89},
    'mchc': {'type': 'number', 'label': 'MCHC', 'unit': 'г/л', 'default': 330},
    'rdw': {'type': 'number', 'label': 'RDW', 'unit': '%', 'default': 12},
    'rdv_sd': {'type': 'number', 'label': 'RDW-SD', 'unit': 'фл', 'default': 45},
    'ret_abs': {'type': 'number', 'label': 'MCHC', 'unit': '×10⁹/л', 'default': 30},

    'ne_abs': {'type': 'number', 'label': 'Нейтрофилы', 'unit': '×10⁹/л', 'default': 3.5},
    'pal': {'type': 'number', 'label': 'Палочкоядерные', 'unit': '%', 'default': 3},
    'seg': {'type': 'number', 'label': 'Сегментоядерные', 'unit': '%', 'default': 57},
    'ly_abs': {'type': 'number', 'label': 'Лимфоциты', 'unit': '×10⁹/л', 'default': 3.5},
    'mo_abs': {'type': 'number', 'label': 'Моноциты', 'unit': '×10⁹/л', 'default': 0.5},
    'eo_abs': {'type': 'number', 'label': 'Эозинофилы', 'unit': '×10⁹/л', 'default': 0.3},
    'ba_abs': {'type': 'number', 'label': 'Базофилы', 'unit': '×10⁹/л', 'default': 0.3},
    'mxd_abs': {'type': 'number', 'label': 'Смеш. фракция', 'unit': '×10⁹/л', 'default': 0.3},

    'mpv': {'type': 'number', 'label': 'MPV', 'unit': 'фл', 'default': 7.5},
    'pdw': {'type': 'number', 'label': 'PDW', 'unit': '%', 'default': 10}
    
}

def process_data(form_data):
    required_results = ["<strong>Обязательные поля:</strong>"]
    additional_results = ["<strong>Дополнительные поля:</strong>"]
    recomendations = ["<br><strong>Рекомендации:</strong>"]

    for field_name, value in form_data.items():
        if field_name in REQUIRED_FIELDS:
            required_results.append(f"{REQUIRED_FIELDS[field_name]['label']}: {value}")
        elif field_name not in ['add_field', 'field_type', 'field_count']:
            additional_results.append(f"{FIELD_TYPES[field_name]['label']}: {value}")
    
    if len(additional_results) == 1:
        # additional_results.append("Нет дополнительных полей")
        additional_results.clear()

    # Тут должен быть вызов функции предсказания и рекомендаций
    recomendations.append(f'выявлено: <font color="red">{predict(form_data.to_dict())}</font>')
    
    return "<br>".join(required_results + additional_results + recomendations)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add_field' in request.form:
            # Обработка добавления нового поля (AJAX запрос)
            field_type = request.form.get('field_type')
            field_key = field_type  # Используем ключ из FIELD_TYPES как имя поля
            
            field_config = FIELD_TYPES.get(field_type, FIELD_TYPES['pregnancy'])
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