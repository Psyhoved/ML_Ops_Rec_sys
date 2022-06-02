"""
Module for build features. This module using functions from clean_data.py script
Requires numpy library
"""
import numpy as np
import pandas as pd

from src.data.clean_data import load_row_data, rename_columns


def make_popularity_abd_sum_list(incoming_data: pd.DataFrame) -> tuple:
    """
    This function make two sorted lists: popularity items and expensive items,
    lists are saved in DF with two columns: item_id and rating (popularity or sum_sale).
    All returns and sales at a price below 1 ruble are filtered out.

    :param incoming_data: DF with row data
    :return: Tuple with two DF sum_list_nom and popularity_list_nom
    """
    popularity_list_nom = incoming_data['item_id'].value_counts().reset_index()
    popularity_list_nom.columns = ['item_id', 'popularity']

    # all returns and sales at a price below 1 ruble are filtered out
    sum_list_nom = incoming_data[incoming_data['sum_sale'] > 1].groupby('item_id')['sum_sale'].mean().reset_index()

    return sum_list_nom, popularity_list_nom


def prepare_ratings(sum_list_nom: pd.DataFrame, popularity_list_nom: pd.DataFrame) -> pd.DataFrame:
    """
    This function make 4 type of ratings for evaluate user-item relation.
    The first two are the amount of money and popularity items among users.
    The other two are log function from the first two.

    There are filtering unpopular items. If less than 10 purchases, the item is deleted

    :param sum_list_nom: DF with rating items by sum sales
    :param popularity_list_nom: DF with rating items by popularity
    :return: DF with 4 types of ratings and other columns
    """
    prep_rating = sum_list_nom.merge(popularity_list_nom, how='left', on='item_id')
    prep_rating = prep_rating[prep_rating['popularity'] >= 10]

    prep_rating['sum_sale_log'] = np.log10(prep_rating['sum_sale'])
    prep_rating['popularity_log'] = np.log10(prep_rating['popularity'])

    return prep_rating


def make_ratings(prep_rating, sum_coef=1, pop_coef=0.5):
    """

    :param prep_rating:
    :param sum_coef:
    :param pop_coef:
    :return:
    """
    prep_rating['rating_sum_S_and_P'] = (sum_coef * prep_rating['sum_sale_log']) + (
            pop_coef * prep_rating['popularity_log'])

    prep_rating['rating_div_S_on_P'] = prep_rating['sum_sale_log'] / prep_rating['popularity_log']
    rating_coef = prep_rating.sort_values(by='rating_div_S_on_P')
    return rating_coef


def prep_data(cleaned_data, rating_coef):
    """

    :param cleaned_data:
    :param rating_coef:
    :return:
    """
    prepare_data = cleaned_data.merge(rating_coef.drop('sum_sale', axis=1),
                                      how='left',
                                      on='item_id').dropna()
    prepare_data['item_id'] = prepare_data['item_id'].str.zfill(7)

    return prepare_data


def build_features(row_data_url):
    """
    
    :param row_data_url:
    :return:
    """
    print('Downloading data from cloud...')
    row_data = load_row_data(row_data_url)
    print("Row data:", row_data)

    print('\n')
    print(80 * '*')
    print('Cleaning data...')

    if 'Период' in row_data.columns:
        incoming_data = rename_columns(row_data)
    else:
        incoming_data = row_data.copy()

    print(80 * '*')
    print('Preparing data for ratings...')
    # lists of mean sum and amount of buys by item
    sum_list_nom, popularity_list_nom = make_popularity_abd_sum_list(incoming_data)

    print(80 * '*')
    print("Generating user's ratings...")
    # make ratings
    prep_rating = prepare_ratings(sum_list_nom, popularity_list_nom)
    rating_coef = make_ratings(prep_rating, sum_coef=1, pop_coef=0.5)
    print(80 * '*')

    print("Prepare data with features")
    rec_sys_data = prep_data(incoming_data, rating_coef)
    return rec_sys_data


if __name__ == "__main__":
    URL = 'https://www.dropbox.com/s/nhswkhngncsi8n6/Data_rec_sys_row.csv?dl=1'
    print(build_features(URL))
