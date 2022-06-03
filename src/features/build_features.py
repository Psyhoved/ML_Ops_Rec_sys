"""
Module for build features. This module using functions from clean_data.py script
Requires numpy library
"""
import numpy as np
import pandas as pd

from src.data.clean_data import load_row_data, rename_columns


def make_sum_and_pop_ratings(incoming_data: pd.DataFrame, target_columns='item_id') -> tuple:
    """
    This function make two sorted lists: popularity items and expensive items,
    lists are saved in DF with two columns: item_id and rating (popularity or sum_sale).
    All returns and sales at a price below 1 ruble are filtered out.

    :param incoming_data: DF with row data
    :param target_columns: str, target item for building recommend system.
    "item_id" if we build recommendations for top goods per user,
    "subgroup_id" if we build recommendations for top groups of item per user

    :return: Tuple with two DF sum_list_nom and popularity_list_nom
    """
    popularity_list_nom = incoming_data[target_columns].value_counts().reset_index()
    popularity_list_nom.columns = [target_columns, 'popularity']

    # all returns and sales at a price below 1 ruble are filtered out
    sum_list_nom = incoming_data[incoming_data['sum_sale'] > 1].groupby(target_columns)['sum_sale'].mean().reset_index()

    return sum_list_nom, popularity_list_nom


def make_ratings(sum_list_nom: pd.DataFrame, popularity_list_nom: pd.DataFrame,
                 sum_coef=1, pop_coef=0.5, target_columns='item_id') -> pd.DataFrame:
    """
    This function make 4 type of ratings for evaluate user-item relation.
    The first two are the amount of money and popularity items among users.
    The other two are logarithm function from the first two.

    There are filtering unpopular items. If less than 10 purchases, the item is deleted.

    The function return 6 types of ratings:
    1. sum_sale - The same ratings that the function get as input;
    2. popularity - The same ratings that the function get as input;
    3. sum_sale_log - logarithm of the sum_sale;
    4. popularity_log - logarithm of the popularity;
    5. rating_sum_S_and_P - sum "sum_sale_log" and "popularity_log" ratings with weights;
    6. rating_div_S_on_P - result of dividing "sum_sale_log" by "popularity_log".

    :param sum_list_nom: DF with rating items by sum sales
    :param popularity_list_nom: DF with rating items by popularity
    :param sum_coef: int, weight for "sum_sale_log", from 0 to 1
    :param pop_coef: int, weight for "popularity_log", from 0 to 1
    :param target_columns: str, target item for building recommend system.
    "item_id" if we build recommendations for top goods per user,
    "subgroup_id" if we build recommendations for top groups of item per user

    :return: DF with 6 types of ratings and item id
    """
    prep_rating = sum_list_nom.merge(popularity_list_nom, how='left', on=target_columns)
    # filtering unpopular items
    prep_rating = prep_rating[prep_rating['popularity'] >= 10]
    # logarithm function for interpreted rating
    prep_rating['sum_sale_log'] = np.log10(prep_rating['sum_sale'])
    prep_rating['popularity_log'] = np.log10(prep_rating['popularity'])

    prep_rating['rating_sum_S_and_P'] = (sum_coef * prep_rating['sum_sale_log']) + (
            pop_coef * prep_rating['popularity_log'])

    prep_rating['rating_div_S_on_P'] = prep_rating['sum_sale_log'] / prep_rating['popularity_log']

    ratings = prep_rating.sort_values(by='rating_sum_S_and_P')
    return ratings


def prep_data(incoming_data: pd.DataFrame, ratings: pd.DataFrame, target_columns='item_id') -> pd.DataFrame:
    """
    This function merge incoming data DF with ratings DF.
    :param incoming_data: DF with incoming information about users, items, group items, stores, etc.
    :param ratings: DF with 6 types of user ratings for items
    :param target_columns: str, target item for building recommend system.
    "item_id" if we build recommendations for top goods per user,
    "subgroup_id" if we build recommendations for top groups of item per user

    :return: merged incoming data and ratings dataframe
    """
    prepare_data = incoming_data.merge(ratings.drop('sum_sale', axis=1),
                                       how='left',
                                       on=target_columns).dropna()

    prepare_data[target_columns] = prepare_data[target_columns].str.zfill(7)

    return prepare_data


def build_features(row_data_url, target_columns='item_id'):
    """

    This function call pipeline for rename columns of row data, if needed,
    generate 6 types of user ratings, and add them to incoming dataframe.

    :param row_data_url: str, URL of row data
    :param target_columns: str, target item for building recommend system.
    "item_id" if we build recommendations for top goods per user,
    "subgroup_id" if we build recommendations for top groups of item per user

    :return: DF with obfuscation information about client, store, goods etc.,
    and 6 types of ratings for user-item recommended system
    """
    print('Downloading data from cloud...')

    # loading row data to pd.DataFrame
    row_data = load_row_data(row_data_url)

    print("Row data:", row_data)

    print('\n')
    print(80 * '*')
    print('Cleaning data...')

    # rename columns if needed
    if 'Период' in row_data.columns:
        incoming_data = rename_columns(row_data)
    else:
        incoming_data = row_data.copy()

    print(80 * '*')
    print('Preparing data for ratings...')

    # lists of mean sum and amount of buys by item
    sum_list_nom, popularity_list_nom = make_sum_and_pop_ratings(incoming_data, target_columns=target_columns)

    print(80 * '*')
    print("Generating user's ratings...")
    # make ratings
    ratings = make_ratings(sum_list_nom, popularity_list_nom, sum_coef=1, pop_coef=0.5, target_columns=target_columns)
    print(80 * '*')

    print("Prepare data with features")
    rec_sys_data = prep_data(incoming_data, ratings, target_columns=target_columns)
    return rec_sys_data


if __name__ == "__main__":
    URL = 'https://www.dropbox.com/s/nhswkhngncsi8n6/Data_rec_sys_row.csv?dl=1'
    print(build_features(URL))
