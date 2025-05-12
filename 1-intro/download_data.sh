#!/bin/bash

BASE_URL="https://d37ci6vzurychx.cloudfront.net/trip-data/"

DATA_PATH="data"

mkdir -p $DATA_PATH

function download_file {

    for i in {1..2}; do
        file_name="yellow_tripdata_2023-0${i}.parquet"
        echo "Attempt to download $file_name"
        # curl -o "/$DATA_PATH/$file_name" "$BASE_URL/$file_name"
        curl -o "$DATA_PATH/$file_name" "$BASE_URL$file_name"
    done
}

download_file