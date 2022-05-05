import pandas as pd

from surprise import SVD

from data_prep import data_preparation
from data_prep import get_top_n
from data_prep import store_sort_df

rozn_rec_data = pd.read_csv('Data_rec_sys_ML_ops.csv')

n = 30
# Выбор данных по конкретному магазину
rozn_rec_data_s1 = store_sort_df(rozn_rec_data, n=n)

# Подготовка данных для surprise
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
