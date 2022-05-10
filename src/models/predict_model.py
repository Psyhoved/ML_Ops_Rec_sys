import pandas as pd
import click
import joblib as jb
from collections import defaultdict
from typing import List
from .prepare_dataset import prepare_dataset


# @click.command()
# @click.argument("input_path", type=click.Path(exists=True))
# @click.argument("output_path", type=click.Path(), nargs=2)
def predict_model(input_paths: List[str], output_path: str, num_predicts):
    prepared_df = prepare_dataset(input_paths[0])
    train_data = prepared_df.build_full_trainset()
    test_data = train_data.build_anti_testset()
    # test_data = pd.read_csv(input_paths[0])
    model = jb.load(input_paths[1])

    print('--------------------------------------------------------------------------')
    print('Генерация рекомендаций')
    print('--------------------------------------------------------------------------')

    # прогноз для тестового датасета
    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    predictions = model.test(test_data)

    # Сохраняем топ-n рекомендаций для каждого юзера в словарь
    # top_n_df = get_top_n(predictions, n_pred=n_pred)

    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:num_predicts]

    with open(output_path, 'w') as f:
        for key, value in top_n.items():
            f.writelines(f"{key}: {value} ")

    print(top_n.items())


if __name__ == '__main__':
    predict_model()

