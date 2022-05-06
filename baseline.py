import pandas as pd

from surprise import SVD

from data_prep import data_preparation
from data_prep import lighter_data
from data_prep import rec_to_df

from model_rec import make_rec

rozn_rec_data = pd.read_csv('Data_rec_sys_ML_ops.csv')

store_n = 55  # позиция магазина в списке ранжированном по кол-ву продаж
n_buy = 5  # минимальное кол-во покупок клиента, для прохождения в алгоритм

# "Облегчаем" данные, оставляя только один магазин и клиентов с n_buy+ покупками
light_data = lighter_data(rozn_rec_data, store_n=store_n, n_buy=n_buy)

data_prep_df = data_preparation(light_data)

# Генерируем top-n рекомендаций для заданных клиентов и номенклатур
top_n = make_rec(data_prep_df,
                 n_pred=10,
                 gridsearch=False,
                 alg=SVD,
                 opt_by='rmse')
# Преобразуем словарь с рекомендациями в таблицу DataFrame
top_n = rec_to_df(top_n)

print(top_n)
