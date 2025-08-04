from flask import Flask, render_template, request, jsonify
from data import FIELDS_DICT, RESULT_DICT, calculate_age
from predict import predict

app = Flask(__name__)

# Обязательные поля с значениями по умолчанию

def process_data(form_data):
    required_results = ["<strong>Обязательные поля:</strong>"]
    additional_results = ["<strong>Дополнительные поля:</strong>"]
    recomendations = ["<br><strong>Рекомендации:</strong>"]

    for field_name, value in form_data.items():
        if field_name == 'gender':
            required_results.append(f"{FIELDS_DICT['required_fields'][field_name]['label']}: {value}")
            age = calculate_age(form_data['birth_date'],
                                form_data['labstudy_date'])
            required_results.append(f"Возраст: {age}")
            continue
        if field_name in ['birth_date', 'labstudy_date']:
            continue
        if field_name in FIELDS_DICT['required_fields']:
            required_results.append(f"{FIELDS_DICT['required_fields'][field_name]['label']}: {value}")
        elif field_name not in ['add_field', 'field_type', 'field_count']:
            additional_results.append(f"{FIELDS_DICT['additional_fields'][field_name]['label']}: {value}")
    
    if len(additional_results) == 1:
        # additional_results.append("Нет дополнительных полей")
        additional_results.clear()

    # Вызов функции предсказания и рекомендаций
    print(form_data.to_dict())
    prediction = RESULT_DICT[predict(form_data.to_dict())[0]]
    recomendations.append(f'Выявлено: <font color="red">{prediction}</font>')
    
    return "<br>".join(required_results + additional_results + recomendations)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add_field' in request.form:
            # Обработка добавления нового поля (AJAX запрос)
            field_type = request.form.get('field_type')
            field_key = field_type  # Используем ключ из FIELDS_DICT['additional_fields'] как имя поля
            
            field_config = FIELDS_DICT['additional_fields'].get(field_type, FIELDS_DICT['additional_fields']['mcv'])
            return jsonify({
                'html': render_template('_field.html', 
                                     field_id=field_key,  # Используем ключ как ID
                                     field_name=field_key,  # Используем ключ как name
                                     field_config=field_config)
            })
        elif 'new_form' in request.form:
            # Показать новую форму
            return render_template('index.html', 
                                field_types=FIELDS_DICT['additional_fields'],
                                required_fields=FIELDS_DICT['required_fields'],
                                result=None,
                                form_submitted=False)
        else:
            # Обработка основной формы
            result = process_data(request.form)
            return render_template('index.html', 
                                field_types=FIELDS_DICT['additional_fields'],
                                required_fields=FIELDS_DICT['required_fields'],
                                result=result,
                                form_submitted=True)
    
    # Первый заход - показать форму с данными по умолчанию
    return render_template('index.html', 
                         field_types=FIELDS_DICT['additional_fields'],
                         required_fields=FIELDS_DICT['required_fields'],
                         result=None,
                         form_submitted=False)

if __name__ == '__main__':
    app.run(debug=True)