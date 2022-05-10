def user_license(light_data):
    """

    :param light_data:
    :return:
    """
    user_license_df = light_data[['user_id', 'Лицензия']]

    all_user_list = user_license_df[['user_id']].drop_duplicates()
    user_with_license_list = user_license_df[user_license_df['Лицензия'] == 1].drop_duplicates()

    # соединяем список всех юзеров со списком юзеров с лицензиями
    user_license_list = all_user_list.merge(user_with_license_list, how='left', on='user_id')
    # у юзеров без лицензии появится nan, заполняем нолями
    user_license_list = user_license_list.fillna(0)
    user_license_list['Лицензия'] = user_license_list['Лицензия'].astype(int)
    # Переименовываем колонку для лучшей интерпретации
    user_license_list = user_license_list.rename(columns={'Лицензия': 'ЛицензияКлиента'})

    return user_license_list


def make_readable_top_n(top_n, light_data, list_unique_nomen):
    """

    :param top_n:
    :param light_data:
    :param list_unique_nomen:
    :return:
    """
    # добавляем название номенклатуры
    top_n_with_nom = top_n.merge(list_unique_nomen, how='left', on='КодНоменклатуры')
    # Определяем клиентов с лицензией
    user_license_list = user_license(light_data)
    # соединяем всё в один датафрейм
    top_n_readable = top_n_with_nom.merge(user_license_list, how='left', on='user_id')
    # раставляем колонки в более удобном порядке
    top_n_readable = top_n_readable[['user_id', 'КодНоменклатуры', 'Номенклатура', 'Оценка', 'ЛицензияКлиента']]
    return top_n_readable
