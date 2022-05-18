from surprise import SVD
import src

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
ALGORITHM:type = SVD
OPTIMISE_BY = "rmse"
NUM_PREDICT = 10


if __name__ == "__main__":
    src.clean_data(RAW_DATA_PATH, CLEANED_DATA_PATH, STORE_POSITION, MIN_NUM_PURCHASES)
    # src.prepare_dataset(CLEANED_DATA_PATH, PREPARED_DATA_PATH)
    src.train_model(CLEANED_DATA_PATH,
                    [MODEL_PATH, CROSS_VAL_RESULTS_PATH],
                    grid_search=GRID_SEARCH,
                    alg=ALGORITHM,
                    opt_by=OPTIMISE_BY)
    src.predict_model([CLEANED_DATA_PATH, MODEL_PATH], PREDICT_DATA_PATH, NUM_PREDICT)

