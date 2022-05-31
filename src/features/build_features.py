"""
add because pylint
Module by build features. This module using functions from clean_data.py script
"""
import numpy as np
import pandas as pd

from src.data.clean_data import load_row_data, clean_data

URL = 'https://www.dropbox.com/s/nhswkhngncsi8n6/Data_rec_sys_row.csv?dl=1'


def make_popularity_abd_sum_list(cleaned_data: pd.DataFrame) -> tuple:
    """

    :param cleaned_data:
    :return:
    """
    popularity_list_nom = cleaned_data['item_id'].value_counts().reset_index()
    popularity_list_nom.columns = ['item_id', 'popularity']
    sum_list_nom = cleaned_data[cleaned_data['sum_sale'] > 1].groupby('item_id')[
        'sum_sale'].mean().reset_index()
    return sum_list_nom, popularity_list_nom


def prepare_ratings(sum_list_nom: pd.DataFrame, popularity_list_nom: pd.DataFrame) -> pd.DataFrame:
    """

    :param sum_list_nom:
    :param popularity_list_nom:
    :return:
    """
    prep_rating = sum_list_nom.merge(popularity_list_nom, how='left', on='item_id')
    prep_rating = prep_rating[prep_rating['popularity'] >= 10]
    prep_rating['sum_sale_log'] = np.log10(prep_rating['sum_sale'])
    prep_rating['popularity_log'] = np.log10(prep_rating['popularity'])

    return prep_rating


def make_ratings(prep_rating: pd.DataFrame, sum_coef=1, pop_coef=0.5) -> pd.DataFrame:
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


def prep_data(cleaned_data: pd.DataFrame, rating_coef: pd.DataFrame) -> pd.DataFrame:
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


def build_features(row_data_url: str) -> pd.DataFrame:
    """

    :param row_data_url:
    :return:
    """
    row_data = load_row_data(row_data_url)
    cleaned_data = clean_data(row_data)

    # lists of mean sum and amount of buys by item
    sum_list_nom, popularity_list_nom = make_popularity_abd_sum_list(cleaned_data)

    # make ratings
    prep_rating = prepare_ratings(sum_list_nom, popularity_list_nom)
    rating_coef = make_ratings(prep_rating, sum_coef=1, pop_coef=0.5)

    rec_sys_data = prep_data(cleaned_data, rating_coef)
    return rec_sys_data


if __name__ == "__main__":
    build_features(URL)
