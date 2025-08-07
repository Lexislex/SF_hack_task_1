"""Это файл для хранения словарей.
Их можно импортировать в любые модули в этой локации.
"""
from datetime import datetime

FIELDS_DICT = {
    'required_fields': {
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
        },
    },
    'additional_fields': {
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
        'pdw': {'type': 'number', 'label': 'PDW', 'unit': '%', 'default': 10},
        
        'plasma': {'type': 'checkbox', 'label': 'Плазматические клетки', 'value': 1,'default': False},
        'plcr': {'type': 'number', 'label': 'P-LCR', 'unit': '%', 'default': 20},
        'myelo': {'type': 'checkbox', 'label': 'Миелоциты', 'value': 1,'default': False},
        'yunye': {'type': 'checkbox', 'label': 'Юные', 'value': 1,'default': False},
        'blasty': {'type': 'checkbox', 'label': 'Бласты', 'value': 1,'default': False},
        'normobl_abs': {'type': 'number', 'label': 'Нормобласты абс.', 'unit': '%', 'default': 0.3},
        'anisocytos': {'type': 'checkbox', 'label': 'Анизоцитоз', 'value': 1,'default': False},
        'hypochromia': {'type': 'checkbox', 'label': 'Гипохромия', 'value': 1,'default': False},
        'macrocytos': {'type': 'checkbox', 'label': 'Макроциоз', 'value': 1,'default': False},
        'microcytos': {'type': 'checkbox', 'label': 'Микроцитоз', 'value': 1,'default': False},
        'poikilocytos': {'type': 'checkbox', 'label': 'Пойкилоцитоз', 'value': 1,'default': False},
        'normoblast': {'type': 'checkbox', 'label': 'Нормобласты', 'value': 1,'default': False},
        'prolym': {'type': 'checkbox', 'label': 'Пролимфоциты', 'value': 1,'default': False},
        'promyelo': {'type': 'checkbox', 'label': 'Промиелоциты', 'value': 1,'default': False},
        
    },
}

# TEST_DATA = {
#     'gender': 'Мужской',
#     'birth_date': '2000-01-01',
#     'labstudy_date': '2025-07-21',
#     'rbc': '4.5',
#     'hgb': '120',
#     'hct': '35',
#     'cp': '0.9',
#     'soe': '7',
#     'wbc': '6.5',
#     'plt': '200',
#     'mcv': '89',
#     'mchc': '330',
#     'rdw': '12',
#     'rdv_sd': '45',
#     'ret_abs': '30',
#     'ne_abs': '3.5',
#     'pal': '3',
#     'seg': '57',
#     'ly_abs': '3.5',
#     'mo_abs': '0.5',
#     'eo_abs': '0.3',
#     'ba_abs': '0.3',
#     'mxd_abs': '0.3',
#     'mpv': '7.5',
#     'pdw': '10',
#     'field_type': 'pdw', 'field_count': '0'
# }

TEST_DATA = {'gender': 'Мужской', 'birth_date': '2000-01-01', 'labstudy_date': '2025-07-21', 'rbc': '4.5', 'hgb': '120', 'hct': '35', 'cp': '0.9', 'soe': '7', 'wbc': '6.5', 'plt': '200', 'field_type': 'mcv', 'field_count': '0'}

REF_COLUMNS = ['age', 'rbc', 'hgb', 'hct', 'mcv', 'mchc', 'rdw', 'rdv_sd', 'ret_abs',
       'cp', 'wbc', 'ne_abs', 'ly_abs', 'mo_abs', 'eo_abs', 'ba_abs', 'pal',
       'seg', 'mxd_abs', 'plasma', 'plt', 'mpv', 'pdw', 'plcr', 'soe', 'myelo',
       'yunye', 'blasty', 'normobl_abs', 'gender', 'anisocytos', 'hypochromia',
       'macrocytos', 'microcytos', 'poikilocytos', 'normoblast', 'prolym', 'promyelo']

RESULT_DICT = {
    0: ['Картина нормального анализа крови','Регулярно проходите диспансеризацию, при появлении жалоб обратитесь к врачу.'],
    1: ['Признаки анемии','Необходима консультация терапевта и прохождение дополнительных исследований'],
    2: ['Признаки воспаления','Если у Вас повышена температура, беспокоят боли срочно обратитесь в неотложное отделенеи поликлиники или в стационар.'],
    3: ['Признаки анемии и воспаления','В ближайшее время необходима консультация терапевта или врача общей практики.'],
    4: ['Признаки онкологического процесса','Необходима консультация онколога или онкогематолога для исключения онкологического процесса'],
}

def calculate_age(birth_date, current_date):
    birth = datetime.strptime(birth_date, "%Y-%m-%d")
    current = datetime.strptime(current_date, "%Y-%m-%d")
    
    age = current.year - birth.year
    # Проверяем, был ли уже день рождения в текущем году
    if (current.month, current.day) < (birth.month, birth.day):
        age -= 1
    return age

if __name__ == '__main__':
    exit(0)