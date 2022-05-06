import pandas as pd

from surprise import SVD
from surprise.model_selection import cross_validate
from surprise.model_selection import GridSearchCV
from data_prep import get_top_n


rozn_rec_data = pd.read_csv('Data_rec_sys_ML_ops.csv')


def gssv(data_prep_df: pd.DataFrame, alg: type, param_grid: dict, measures, opt_by="rmse"):
    """

    :param data_prep_df:
    :param alg:
    :param param_grid:
    :param measures:
    :param opt_by:
    :return:
    """
    print('Проводится GridSearch')

    gs = GridSearchCV(alg, param_grid, measures=measures, cv=3)
    gs.fit(data_prep_df)

    print('--------------------------------------------------------------------------')
    # best RMSE score
    print(f'best_score {opt_by}: {gs.best_score[opt_by]}')
    # combination of parameters that gave the best RMSE score
    print(f'best_params {opt_by}: {gs.best_params[opt_by]}')

    print('--------------------------------------------------------------------------')

    return gs


def make_rec(data_prep_df: pd.DataFrame, n_pred=10,
             gridsearch=True, alg: type = SVD,
             opt_by='rmse'):
    """

    :param data_prep_df:
    :param n_pred:
    :param gridsearch:
    :param alg:
    :param opt_by:
    :return:
    """
    measures = ['RMSE', 'MAE']
    # тренировочные данные
    trainset = data_prep_df.build_full_trainset()

    # Опциональнй гридсёрч по заданным параметрам
    if gridsearch:
        # подбор оптимальных параметров модели by gridsearch
        param_grid = {'n_epochs': [10, 20, 30], 'lr_all': [0.002, 0.005, 0.01],
                      'reg_all': [0.02, 0.4, 0.6]}

        gs = gssv(alg=SVD, param_grid=param_grid,
                  measures=measures,
                  data_prep_df=data_prep_df, opt_by=opt_by)

        # We can now use the algorithm that yields the best rmse:
        algo = gs.best_estimator['rmse']
        algo.fit(trainset)

    else:
        # обучение алгоритма
        algo = alg()  # KNNBasic()
        algo.fit(trainset)

        print('Проводится Кроссвалидация')
        print('--------------------------------------------------------------------------')

        # кроссвалидация
        cross_validate(algo, data_prep_df, measures=measures, cv=4, verbose=True)

    # Подготовка тестового датасета
    testset = trainset.build_anti_testset()

    print('--------------------------------------------------------------------------')
    print('Генерация рекомендаций')
    print('--------------------------------------------------------------------------')

    # прогноз для тестового датасета
    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    predictions = algo.test(testset)

    # Сохраняем топ-n рекомендаций для каждого юзера в словарь
    top_n_df = get_top_n(predictions, n_pred=n_pred)

    return top_n_df
