"""
add because pylint
This module load and clean row data
Requires pandas library
"""
# -*- coding: utf-8 -*-
import pandas as pd


def load_row_data(row_data_url: str) -> pd.DataFrame:
    """
    This function uploads csv-file with row data from url, read it by pandas and converts columns type.
    :param row_data_url: url link of csv-file in dropdox (or other cloud)
    :return: pd.DataFrame
    """
    row_data = pd.read_csv(row_data_url, converters={'subgroup_id': str, 'user_id': str, 'item_id': str})
    return row_data


def rename_columns(row_data: pd.DataFrame) -> pd.DataFrame:
    """
    This function rename columns of incoming file according to the established template
    :param row_data:
    :return:
    """
    # arrange columns in more convenient order
    incoming_data = row_data[['Период', 'user_id', 'КодМагазина', 'КодНоменклатуры', 'id_subgroup',
                              'Сумма', 'ABC_анализ_Номенклатура', 'Лицензия']]

    # rename columns
    incoming_data.columns = ['datetime', 'user_id', 'store_id', 'item_id', 'subgroup_id',
                             'sum_sale', 'ABC_analise_item', 'license']
    return incoming_data
