import pandas as pd
import click
import joblib as jb
from surprise import SVD
from surprise.model_selection import GridSearchCV
from surprise.model_selection import cross_validate
from typing import List
from .prepare_dataset import prepare_dataset


MEASURES = ['RMSE', 'MAE']
PARAM_GRID = {'n_epochs': [10, 20, 30],
              'lr_all': [0.002, 0.005, 0.01],
              'reg_all': [0.02, 0.4, 0.6]}  # подбор оптимальных параметров модели by grid_search


# @click.command()
# @click.argument("input_paths", type=click.Path(exists=True), nargs=2)
# @click.argument("output_paths", type=click.Path(), nargs=2)
# @click.argument("grid_search", type=click.BOOL)
# @click.argument("alg", type=click.types)
# @click.argument("opt_by", type=click.STRING)
def train_model(input_path: str, output_paths: List[str], grid_search=True, alg: type = SVD, opt_by='rmse'):
    # тренировочные данные
    prepared_df = prepare_dataset(input_path)
    train_data = prepared_df.build_full_trainset()
    # test_data = train_data.build_anti_testset()
    # Опциональнй гридсёрч по заданным параметрам
    if grid_search:
        print('Проводится GridSearch')

        gs = GridSearchCV(alg, PARAM_GRID, measures=MEASURES, cv=3)
        gs.fit(prepared_df)  # Почему делааем гридсерч на всех данных? Проверить качество при обучекнии на x_train

        print(80*'-')
        print(f'best_score {opt_by}: {gs.best_score[opt_by]}')
        print(f'best_params {opt_by}: {gs.best_params[opt_by]}')

        print(80*'-')

        # We can now use the algorithm that yields the best rmse:
        model = gs.best_estimator['rmse']
        model.fit(train_data)

    else:
        # обучение алгоритма
        model = alg()  # KNNBasic()
        model.fit(train_data)

        print('Проводится Кроссвалидация')
        print(80*'-')

        # кроссвалидация
        cross_val_results = cross_validate(model, prepared_df, measures=MEASURES, cv=4, verbose=True)
        # print(cross_val_results)
        with open(output_paths[1], 'w') as f:
            for key, value in cross_val_results.items():
                f.writelines(f"{key}: {value} ")

    jb.dump(model, output_paths[0])


if __name__ == '__main__':
    train_model()


