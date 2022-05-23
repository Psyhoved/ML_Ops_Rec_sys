# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import streamlit as st
import click


# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
# @click.argument('store_position', type=click.INT)
# @click.argument('min_num_purchases', type=click.INT)
def clean_data(input_path: str, output_path: str, store_position: int, min_num_purchases: int):
    df = pd.read_csv(input_path,
                     header=0,
                     names=['period', 'user_id', 'store_id', 'item_id', 'license', 'type_by_nomenclature',
                            'rating'],
                     dtype={'user_id': np.str,
                            'store_id': np.str,
                            'item_id': np.str,
                            'license': np.int8,
                            'type_by_nomenclature': np.str,
                            'rating': np.int32})
    st.write('Dataframe clean starts')

    # deleting spaces in string columns
    df['user_id'] = df['user_id'].str.strip()
    df['store_id'] = df['store_id'].str.strip()
    df['item_id'] = df['item_id'].str.strip()

    # delete strange user_id.
    # EDIT THIS ROW FOR ANOTHER CLEAN FILTER
    df_clear = df[df.user_id.str.len() == 13]

    # getting an id store placed on :store_position place in store list sorted by purchases
    # получение идентификатора магазина, размещенного на месте :store_position в списке магазинов,
    # отсортированном по покупкам
    store = df_clear['store_id'].value_counts().index[store_position]

    # getting purchasing data by selected store
    # получение данных о покупках по выбранному магазину
    one_store_data = df_clear[df_clear['store_id'] == store]

    st.write(f'Data collected for the store ranked {store_position} in terms of sales')

    # print(f'Data collected for the store ranked {store_position} in terms of sales')
    # print(f'Данные по магазину, занимающему {store_position}-е место по кол-ву продаж, собраны')
    # print('--------------------------------------------------------------------------')

    users_by_purchases = one_store_data['user_id'].value_counts().reset_index()
    users_by_purchases = users_by_purchases.rename(columns={'index': 'user_id', 'user_id': 'purchases'})
    users_id_list = users_by_purchases[users_by_purchases['purchases'] > min_num_purchases]['user_id']
    users_filter = one_store_data['user_id'].isin(users_id_list)
    cleaned_data = one_store_data[users_filter]

    cleaned_data.to_csv(output_path, index=False)


if __name__ == "__main__":
    clean_data()
