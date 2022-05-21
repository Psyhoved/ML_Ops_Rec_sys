import streamlit as st
import pandas as pd
import numpy as np


def visualize(input_path: str):
    df = pd.read_csv(input_path,
                     header=0,
                     names=['period', 'user_id', 'store_id', 'item_id', 'license', 'type_by_nomenclature', 'rating'],
                     dtype={'user_id': np.str,
                            'store_id': np.str,
                            'item_id': np.str,
                            'license': np.int8,
                            'type_by_nomenclature': np.str,
                            'rating': np.int32})

    st.write(df.head())
