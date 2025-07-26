from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Группировка полей по категориям
REQUIRED_FIELDS = {
    'patient': {
        'sex': {
            'type': 'select', 
            'label': 'Пол', 
            'required': True,
            'options': ['Муж.', 'Жен.'], 
            'default': 'Муж.',
            'tooltip': 'Биологический пол пациента'
        },
        'birth_date': {
            'type': 'date', 
            'label': 'Дата рождения', 
            'required': True, 
            'default': '2000-01-01',
            'tooltip': 'Формат: ГГГГ-ММ-ДД'
        }
    },
    'red_blood': {
        'hemoglobin': {
            'type': 'number', 
            'label': 'Гемоглобин', 
            'default': 120,
            'unit': 'г/л',
            'required': True,
            'tooltip': 'Норма: 130-160 (м), 120-140 (ж)'
        },
        'erythrocytes': {
            'type': 'number',
            'label': 'Эритроциты',
            'default': 4.5,
            'unit': '×10¹²/л',
            'required': True,
            'tooltip': 'Норма: 4.0-5.1 (м), 3.7-4.7 (ж)'
        }
    },
    'white_blood': {
        'leukocytes': {
            'type': 'number',
            'label': 'Лейкоциты',
            'default': 6.5,
            'unit': '×10⁹/л',
            'required': True,
            'tooltip': 'Норма: 4.0-9.0'
        }
    },
    'platelets': {
        'platelets_count': {
            'type': 'number',
            'label': 'Тромбоциты',
            'default': 250,
            'unit': '×10⁹/л',
            'required': True,
            'tooltip': 'Норма: 180-320'
        }
    }
}

FIELD_TYPES = {
    'patient': {
        'allergy': {'type': 'text', 'label': 'Аллергии', 'default': ''},
        'medication': {'type': 'text', 'label': 'Приём препаратов', 'default': ''}
    },
    'red_blood': {
        'mch': {'type': 'number', 'label': 'MCH', 'unit': 'пг', 'default': 27},
        'mchc': {'type': 'number', 'label': 'MCHC', 'unit': 'г/л', 'default': 330}
    },
    'white_blood': {
        'neutrophils': {'type': 'number', 'label': 'Нейтрофилы', 'unit': '%', 'default': 55},
        'lymphocytes': {'type': 'number', 'label': 'Лимфоциты', 'unit': '%', 'default': 35}
    },
    'platelets': {
        'mpv': {'type': 'number', 'label': 'MPV', 'unit': 'фл', 'default': 7.5},
        'pdw': {'type': 'number', 'label': 'PDW', 'unit': '%', 'default': 10}
    }
}

def calculate_age(birth_date_str):
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None

def process_data(form_data):
    results = {
        'patient': ["<strong>Данные пациента:</strong>"],
        'red_blood': ["<strong>Красная кровь:</strong>"],
        'white_blood': ["<strong>Белая кровь:</strong>"],
        'platelets': ["<strong>Тромбоциты:</strong>"]
    }
    
    for field_name, value in form_data.items():
        # Пропускаем служебные поля
        if field_name in ['add_field', 'field_type', 'field_count', 'new_form', 'section']:
            continue
            
        # Проверяем обязательные поля
        field_found = False
        for section, fields in REQUIRED_FIELDS.items():
            if field_name in fields:
                field_config = fields[field_name]
                if field_name == 'birth_date':
                    age = calculate_age(value)
                    age_text = f" (Возраст: {age} лет)" if age else ""
                    results['patient'].append(f"{field_config['label']}: {value}{age_text}")
                else:
                    results[section].append(f"{field_config['label']}: {value}")
                field_found = True
                break
                
        # Если поле не обязательное, определяем его секцию по имени
        if not field_found:
            if field_name.startswith('patient_'):
                field_label = field_name.replace('patient_', '').replace('_', ' ').title()
                results['patient'].append(f"{field_label}: {value}")
            elif field_name.startswith('red_'):
                field_label = field_name.replace('red_', '').replace('_', ' ').title()
                results['red_blood'].append(f"{field_label}: {value}")
            elif field_name.startswith('white_'):
                field_label = field_name.replace('white_', '').replace('_', ' ').title()
                results['white_blood'].append(f"{field_label}: {value}")
            elif field_name.startswith('platelets_'):
                field_label = field_name.replace('platelets_', '').replace('_', ' ').title()
                results['platelets'].append(f"{field_label}: {value}")
            else:
                # Если поле не подходит ни к одной категории
                results['patient'].append(f"{field_name}: {value}")
    
    # Собираем итоговый результат, пропуская пустые секции
    final_result = []
    for section, items in results.items():
        if len(items) > 1:  # Если есть данные кроме заголовка
            final_result.extend(items)
            final_result.append("")  # Пустая строка между секциями
    
    return "<br>".join(final_result).strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add_field' in request.form:
            section = request.form.get('section')
            field_type = request.form.get('field_type')
            field_config = FIELD_TYPES[section].get(field_type)
            
            # Проверяем, не было ли уже добавлено такое поле
            existing_fields = request.form.getlist('existing_fields')
            field_id = f"{section}_{field_type}"
            
            if field_id in existing_fields:
                return jsonify({'error': 'Это поле уже добавлено'}), 400
            
            return jsonify({
                'html': render_template('_field.html',
                                     field_id=field_id,
                                     field_name=field_type,
                                     field_config=field_config,
                                     section=section)
            })
        elif 'new_form' in request.form:
            return render_template('index.html',
                                required_fields=REQUIRED_FIELDS,
                                field_types=FIELD_TYPES,
                                result=None)
        else:
            result = process_data(request.form)
            return render_template('index.html',
                                required_fields=REQUIRED_FIELDS,
                                field_types=FIELD_TYPES,
                                result=result)
    
    return render_template('index.html',
                         required_fields=REQUIRED_FIELDS,
                         field_types=FIELD_TYPES,
                         result=None)

if __name__ == '__main__':
    app.run(debug=True)