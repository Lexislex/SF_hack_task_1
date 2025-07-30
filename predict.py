import os
import joblib
import pandas as pd
import numpy as np
# from keras import saving
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from data import TEST_DATA, REF_COLUMNS, FIELDS_DICT, calculate_age

def check_columns(df: pd.DataFrame, reference_columns: list[str], verbouse: bool=True) -> tuple:
    """Проверяет, соответствуют ли столбцы DataFrame эталонному списку.

    Сравнивает названия столбцов переданного DataFrame с эталонным списком.
    Возвращает `True`, если все столбцы совпадают, и `False`, если есть различия.
    В случае несоответствия выводит в консоль информацию о недостающих/лишних столбцах.

    Args:
        df: DataFrame, который нужно проверить.
        reference_columns: Список эталонных названий столбцов.
        verbose: Вывод в консоль несоответствий.

    Returns:
        tuple: (True,) если столбцы идентичны.

        (False, missing_columns, extra_columns) если есть различия.
    """
    df_columns = list(df.columns)
    
    if set(df_columns) == set(reference_columns):
        return (True,)
        
    missing_columns = set(reference_columns) - set(df_columns)
    extra_columns = set(df_columns) - set(reference_columns)
    
    if verbouse:
        if missing_columns:
            print(f"Отсутствуют столбцы: {missing_columns}")
        if extra_columns:
            print(f"Лишние столбцы: {extra_columns}")

    return False, missing_columns, extra_columns

def preprocess_df(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Проводит препроцессинг набора данных для предсказания.

    Удаляет неинформативные признаки.
    # Кодирует категориальные признаки.
    Стандартизирует числовые признаки.

    Args:
        df_clean: Набор данных, который нужно подготовить для предсказания.

    Returns:
        pd.DataFrame: Подготовленный набор данных.
    """
    bool_col = ['gender', 'anisocytos', 'hypochromia',
            'macrocytos','microcytos', 'poikilocytos',
            'normoblast', 'promyelo']

    num_col = ['age', 'rbc', 'hgb', 'hct', 'mcv', 'mchc', 'rdw',
            'rdv_sd', 'ret_abs', 'cp', 'wbc', 'ne_abs', 'ly_abs',
            'mo_abs', 'eo_abs', 'ba_abs', 'pal', 'seg', 'mxd_abs',
            'plasma', 'plt', 'mpv', 'pdw', 'plcr', 'soe', 'myelo',
            'yunye', 'blasty', 'normobl_abs']

    # Кодируем категориальные переменные

    
    # Стандартизация числовых признаков в тренировочном и валидационном наборе
    numeric_data = df_clean[num_col].copy()
    min_max = MinMaxScaler()
    scaled_features = min_max.fit_transform(numeric_data)
    normalized_data = pd.DataFrame(scaled_features, columns=numeric_data.columns)
    df_clean = pd.concat([normalized_data, df_clean[bool_col]], axis=1)

    return df_clean

def preprocess_dict(data_dict):
    del data_dict['field_type'], \
        data_dict['field_count']
    birth_date = data_dict.pop('birth_date', None)
    labstudy_date = data_dict.pop('labstudy_date', None)
    data_dict['age'] = calculate_age(birth_date, labstudy_date)
    data_dict['gender'] = 1 if data_dict.get('gender') == 'Мужской' else 0

    for el in REF_COLUMNS:
        if el not in data_dict:
            for section, fields in FIELDS_DICT.items():
                for field_name, config in fields.items():
                    if field_name == el:
                        data_dict[el] = config['default']
                        break

    return data_dict

def predict(form_data):
    try:
        form_data = preprocess_dict(form_data)
        df = pd.DataFrame({k: [v] for k, v in form_data.items()})
        # print(df)
        if not check_columns(df, REF_COLUMNS)[0]:
            raise Exception('Неверная структура полей:')
        # print('✅ Файл успешно загружен.')
        # print(df.T)
        X = preprocess_df(df)
        # print('✅ Препроцессинг данных успешно завершен.')

        model = joblib.load('inference/best_model.pkl')
        y_pred = model.predict(X)
        return y_pred[0]
    except Exception as e:
        print(f'{e} ❌ Возникла ошибка!')
        exit()

if __name__ == "__main__":
    print(predict(TEST_DATA))