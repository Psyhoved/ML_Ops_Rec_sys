"""
unit-test for build_feature function
"""
from collections import Counter
from src.features import build_features


def test_build_features(row_data_url):
    """
    unit-test for build_feature function
    :param row_data_url:
    :return:
    """
    rozn_rec_data_r = build_features(row_data_url)
    list_columns = ['datetime', 'user_id', 'store_id', 'item_id', 'sum_sale', 'quantity',
                    'license', 'ABC_analise_item', 'id_subgroup', 'popularity', 'sum_sale_log',
                    'popularity_log', 'rating_sum_S_and_P', 'rating_div_S_on_P']

    assert Counter(rozn_rec_data_r.columns) == Counter(list_columns)
