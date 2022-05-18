from ..data.user_license import user_license


def make_readable_top_n(top_n, light_data, nomenclature_list):
    """

    :param top_n:
    :param light_data:
    :param nomenclature_list:
    :return:
    """

    # добавляем название номенклатуры
    top_n_with_nom = top_n.merge(nomenclature_list, how='left', on='КодНоменклатуры')
    # Определяем клиентов с лицензией
    user_license_list = user_license(light_data)
    # соединяем всё в один датафрейм
    top_n_readable = top_n_with_nom.merge(user_license_list, how='left', on='user_id')
    # раставляем колонки в более удобном порядке
    top_n_readable = top_n_readable[['user_id', 'КодНоменклатуры', 'Номенклатура', 'Оценка', 'ЛицензияКлиента']]

    return top_n_readable
