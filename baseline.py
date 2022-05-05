import pandas as pd

from surprise import SVD

from data_prep import data_preparation
from data_prep import get_top_n

rozn_rec_data = pd.read_csv('Data_rec_sys_ML_ops.csv')

n = 30

print('Подготовка датафрейма')
# магазин с наибольшим числом покупок
store = rozn_rec_data['КодМагазина'].value_counts().index[n]
# Оставляем данные только по одному магазину
rozn_rec_data_s1 = rozn_rec_data[rozn_rec_data['КодМагазина'] == store]

print(f'Данные по магазину, занимающему {n}-е место по кол-ву продаж, собраны')
print('Подготовка trainset')
# Подготовка данных
data_prep = data_preparation(rozn_rec_data_s1)
trainset = data_prep.build_full_trainset()

print('Обучение алгоритма')
# обучение алгоритма
algo = SVD()  # KNNBasic()
algo.fit(trainset)

print('Подготовка testset')
# Подготовка тестового датасета
testset = trainset.build_anti_testset()
print('формирование прогноза')
# прогноз для тестового датасета
# Than predict ratings for all pairs (u, i) that are NOT in the training set.
predictions = algo.test(testset)

print('Вывод top-n рекомендаций')
# Сохраняем топ-n рекомендаций для каждого юзера в словарь
top_n = get_top_n(predictions, n_pred=10)

print(top_n)
