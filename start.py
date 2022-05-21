from surprise import SVD
import streamlit as st
import src
import warnings


warnings.filterwarnings('ignore')


st.title('Individual selection of products for the client')


RAW_DATA_PATH = "data/raw/market_sales.csv"
CLEANED_DATA_PATH = "data/interim/data_cleaned.csv"
PREPARED_DATA_PATH = "data/processed/prepared_data.csv"
# PREPARED_DATA_PATH_TEST = "data/processed/test_data.csv"
MODEL_PATH = "models/svd_model.pkl"
CROSS_VAL_RESULTS_PATH = "reports/cross_val_results.txt"
PREDICT_DATA_PATH = "data/external/recommendations.csv"

STORE_POSITION = 50  # store position in the list ranked by number of sales
MIN_NUM_PURCHASES = 10  # the minimum number of purchases to pass into the algorithm
GRID_SEARCH = False
ALGORITHM: type = SVD
OPTIMISE_BY = "rmse"
NUM_PREDICT = 10


if __name__ == "__main__":
    store_position = st.number_input('Store position in the list ranked by number of sales',
                                     min_value=1,
                                     value=STORE_POSITION,
                                     step=1,
                                     format='%d')
    min_num_purchases = st.number_input('How much purchases user should have?',
                                        min_value=1,
                                        value=MIN_NUM_PURCHASES,
                                        step=1,
                                        format='%d')
    use_GS = st.checkbox('Do you need to use a GridSearch?', value=GRID_SEARCH)
    algorithm = st.text_input('Type of algorithm') # Should to use st.select
    optimise_by = st.selectbox(
        'How would you like to optimise algorithm?',
        (OPTIMISE_BY, 'mse'))
    num_predict = st.number_input('How many elements to predict?',
                                     min_value=1,
                                     value=NUM_PREDICT,
                                     step=1,
                                     format='%d')

    st.write(num_predict)

    if st.button("Get predictions"):
        src.clean_data(RAW_DATA_PATH, CLEANED_DATA_PATH, store_position, min_num_purchases)
        # src.prepare_dataset(CLEANED_DATA_PATH, PREPARED_DATA_PATH)
        src.train_model(CLEANED_DATA_PATH,
                        [MODEL_PATH, CROSS_VAL_RESULTS_PATH],
                        grid_search=use_GS,
                        alg=ALGORITHM,
                        opt_by=optimise_by)
        src.predict_model([CLEANED_DATA_PATH, MODEL_PATH], PREDICT_DATA_PATH, num_predict)
    # with st.spinner('Cleaning data, please wait...'):
    # src.clean_data(RAW_DATA_PATH, CLEANED_DATA_PATH, store_position, min_num_purchases)
    # # st.write('Data collected for the store ranked 50 in terms of sales')
    # # # src.prepare_dataset(CLEANED_DATA_PATH, PREPARED_DATA_PATH)
    # src.train_model(CLEANED_DATA_PATH,
    #                 [MODEL_PATH, CROSS_VAL_RESULTS_PATH],
    #                 grid_search=use_GS,
    #                 alg=ALGORITHM,
    #                 opt_by=optimise_by)
    # src.predict_model([CLEANED_DATA_PATH, MODEL_PATH], PREDICT_DATA_PATH, num_predict)

