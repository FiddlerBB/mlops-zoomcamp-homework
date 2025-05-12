import polars as pl
from polars import DataFrame
from rich import print as rich
import logging
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge

from sklearn.metrics import root_mean_squared_error


data_path = "data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


logger = logging.getLogger(__name__)
class Intro:
    def __init__(self):
        self.data_path = data_path
        self.df_jan = pl.read_parquet(f"{self.data_path}/yellow_tripdata_2023-01.parquet")
        self.df_feb = pl.read_parquet(f"{self.data_path}/yellow_tripdata_2023-02.parquet")

    def question_1(self):
        logger.info(f"Total columns: {len(self.df_jan.columns)}")

        return 
    
    def question_2(self):
        self.df_jan = self.df_jan.lazy().with_columns(
            (pl.col("tpep_dropoff_datetime") - pl.col("tpep_pickup_datetime")).alias("duration")
        ).collect()
        logger.info(f"Standard deviation: {self.df_jan.select(pl.std('duration'))}")

    def question_3(self):
        ori_df_jan_len = len(self.df_jan)
        df_jan_filtered = self.df_jan.filter(
            (pl.col("duration").dt.total_minutes() >= 1) & (pl.col("duration").dt.total_minutes() <= 60))
        filtered_df_jan_len = len(df_jan_filtered)
        logger.info(f"percentage of records with duration between 1 and 60 minutes: {filtered_df_jan_len / ori_df_jan_len * 100:.2f}%")
        self.df_jan_filtered = df_jan_filtered

    def question_4(self):
        categories = ["PULocationID", "DOLocationID"]
        numerical = ['trip_distance']

        self.df_jan_filtered = self.df_jan_filtered.with_columns(
            [pl.col(col).cast(pl.String) for col in categories]
        )
        train_dict = self.df_jan_filtered.select(categories + numerical).to_dicts()

        dv = DictVectorizer()
        X_train = dv.fit_transform(train_dict)
        target = 'duration'

        y_train = self.df_jan_filtered.select(pl.col(target).dt.total_minutes()).to_series().to_list()
        lr = LinearRegression()
        lr.fit(X_train, y_train)

        y_pred = lr.predict(X_train)

        mse = root_mean_squared_error(y_train, y_pred)
        logger.info(f"RMSE: {mse:.2f}")

    def train_model(self, df: DataFrame):
        categories = ["PULocationID", "DOLocationID"]
        numerical = ['trip_distance']
        df = df.lazy().with_columns(
            (pl.col("tpep_dropoff_datetime") - pl.col("tpep_pickup_datetime")).alias("duration")
        ).collect()

        df = df.lazy().with_columns(
            (pl.col("duration").dt.total_minutes()).alias("duration")
        ).collect()
        df = df.filter(
            (pl.col("duration") >= 1) & (pl.col("duration") <= 60))
        
        df = df.with_columns(
            [pl.col(col).cast(pl.String) for col in categories]
        )
        print(df.head())
        return df
    
    def question_5(self):
        df_train = self.train_model(self.df_jan)
        df_val = self.train_model(self.df_feb)
        df_train = df_train.lazy().with_columns(
            (pl.col('PULocationID') + '_' + pl.col('DOLocationID')).alias('PU_DO')).collect()
        df_val  = df_val.lazy().with_columns(
            (pl.col('PULocationID') + '_' + pl.col('DOLocationID')).alias('PU_DO')).collect()
        categories = ["PU_DO"]
        numerical = ['trip_distance']
        dv = DictVectorizer()
        train_dict = df_train.select(categories + numerical).to_dicts()
        X_train = dv.fit_transform(train_dict)
        val_dict = df_val.select(categories + numerical).to_dicts()
        X_val = dv.transform(val_dict)
        target  = 'duration'
        y_train = df_train.select(pl.col(target)).to_series().to_list()
        y_val = df_val.select(pl.col(target)).to_series().to_list() 
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        y_pred = lr.predict(X_train)

        train_mse = root_mean_squared_error(y_train, y_pred)
        logger.info(f"TrainRMSE: {train_mse:.2f}")

        lr = Lasso(0.01)
        lr.fit(X_val, y_val)

        y_pred = lr.predict(X_val)

        val_mse = root_mean_squared_error(y_val, y_pred)
        logger.info(f"ValRMSE: {val_mse:.2f}")

         


def main():
    intro = Intro()
    
    # intro.question_1()
    # intro.question_2()
    # intro.question_3()
    # intro.question_4()
    intro.question_5()
if __name__ == "__main__":
    main()