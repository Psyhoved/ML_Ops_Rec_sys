import click
import pandas as pd
from surprise import Reader
from surprise import Dataset
import streamlit as st
from typing import List


# @click.command()
# @click.argument("input_filepath", type=click.Path(exists=True))
# @click.argument("output_file_paths", type=click.Path(), nargs=2)
def prepare_dataset(input_filepath: str):
    df = pd.read_csv(input_filepath)

    st.write('Preparing data...')

    # print('Подготовка данных')
    # print('--------------------------------------------------------------------------')

    prepared_df = df[['user_id', 'item_id', 'rating']].reset_index(drop=True)

    # A reader is still needed but only the rating_scale param is required.
    reader = Reader(rating_scale=(1, 10))
    prepared_df = Dataset.load_from_df(prepared_df[['user_id', 'item_id', 'rating']], reader)

    # train_data = prepared_df.build_full_trainset()
    # test_data = train_data.build_anti_testset()
    # train_data.to_csv(output_paths[0], index=False)
    # test_data.to_csv(output_paths[1], index=False)

    return prepared_df


if __name__ == '__main__':
    prepare_dataset()
