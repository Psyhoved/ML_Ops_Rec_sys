import pandas as pd


def user_license(input_path: str):
    """
    :param input_path:
    :return:
    """
    light_data = pd.read_csv(input_path)

    user_license_df = light_data[['user_id', 'license']]

    all_user_list = user_license_df[['user_id']].drop_duplicates()
    user_with_license_list = user_license_df[user_license_df['license'] == 1].drop_duplicates()

    # соединяем список всех юзеров со списком юзеров с лицензиями
    user_license_list = all_user_list.merge(user_with_license_list, how='left', on='user_id')
    # у юзеров без лицензии появится nan, заполняем нолями
    user_license_list = user_license_list.fillna(0)
    user_license_list['license'] = user_license_list['license'].astype(int)
    # Переименовываем колонку для лучшей интерпретации
    user_license_list = user_license_list.rename(columns={'license': 'client_license'})

    return user_license_list
