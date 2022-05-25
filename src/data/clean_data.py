"""
add because pylint
This module load and clean row data
"""
# -*- coding: utf-8 -*-
import pandas as pd


def load_row_data(row_data_url: str):
    """

    Args:
        row_data_url:

    Returns:

    """
    row_data = pd.read_csv(row_data_url, converters={'id_subgroup': str, 'user_id': str})
    return row_data


def clean_data(row_data):
    """

    Args:
        row_data:

    Returns:

    """
    # arrange columns in more convenient order
    cleaned_data = row_data[['Период', 'user_id', 'КодМагазина', 'КодНоменклатуры', 'id_subgroup',
                             'Сумма', 'ABC_анализ_Номенклатура', 'Лицензия']]

    # rename columns
    cleaned_data.columns = ['datetime', 'user_id', 'store_id', 'item_id', 'subgroup_id',
                            'sum_sale', 'ABC_analise_item', 'license']
    return cleaned_data


if __name__ == "__main__":
    clean_data()
