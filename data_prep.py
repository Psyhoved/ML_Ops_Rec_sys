import pandas as pd
from surprise import Reader
from surprise import Dataset
from collections import defaultdict


def clear_one_buy_client(df: pd.DataFrame, n_buy=10) -> pd.DataFrame:
    """ Функция очищает датафрейм от клиентов,
      которые сделали меньше n покупок

      parameters:
      df (pd.DataFrame): датафрейм, который нужно очистить
      n (int): Число покупок, по которому отсеиваются клиенты

      return:
      pd.DataFrame: очищенный датафрейм
    """
    a = df['user_id'].value_counts().reset_index()
    df_less_10 = a[a['user_id'] > n_buy]
    df_less_10 = df_less_10[['index']].rename(columns={'index': 'user_id'})
    return df_less_10.merge(df)


def data_preparation(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """
    print('Подготовка trainset')

    data_prep = df[['user_id', 'КодНоменклатуры', 'rating']].reset_index(drop=True)
    data_prep = data_prep.rename(columns={'user_id': 'userID', 'КодНоменклатуры': 'itemID'})

    # A reader is still needed but only the rating_scale param is requiered.
    reader = Reader(rating_scale=(1, 10))
    data_prep = Dataset.load_from_df(data_prep[['userID', 'itemID', 'rating']], reader)
    return data_prep


# Функция для вывода топ-N рекомендаций для каждого пользователя
def get_top_n(predictions: list, n_pred=10) -> dict:
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n_pred(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n_pred]

    return top_n


def rec_to_df(top_n: dict) -> pd.DataFrame:
    """

    :param top_n:
    :return:
    """
    # Сохраняем всё в один датафрейм
    recomend_rate_df = pd.DataFrame()
    for elem in top_n.keys():
        rate_df = pd.DataFrame(top_n[elem],
                               columns=['Номенлатура', 'Оценка'])
        rate_df['Клиент'] = elem
        recomend_rate_df = pd.concat([recomend_rate_df, rate_df])
    # расставляем колонки в нужном порядке
    recomend_rate_df = recomend_rate_df[['Клиент', 'Номенлатура', 'Оценка']]
    return recomend_rate_df


def store_sort_df(df: pd.DataFrame, store_n=50) -> pd.DataFrame:
    """

    :param df:
    :param store_n:
    :return:
    """
    print('Подготовка датафрейма')
    print('--------------------------------------------------------------------------')

    # магазин с наибольшим числом покупок
    store = df['КодМагазина'].value_counts().index[store_n]
    # Оставляем данные только по одному магазину
    rozn_rec_data_s1 = df[df['КодМагазина'] == store]

    print(f'Данные по магазину, занимающему {store_n}-е место по кол-ву продаж, собраны')
    print('--------------------------------------------------------------------------')

    return rozn_rec_data_s1


def lighter_data(df: pd.DataFrame, store_n=50, n_buy=10) -> pd.DataFrame:
    """

    :param df:
    :param store_n:
    :param n_buy:
    :return:
    """
    # выбор магазина для генерации рекомендаций
    rozn_rec_data_s1 = store_sort_df(df, store_n=store_n)
    rozn_rec_data_s1 = clear_one_buy_client(rozn_rec_data_s1, n_buy=n_buy)
    return rozn_rec_data_s1
