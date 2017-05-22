call gsutil cp Wline_bor_date_header.csv gs://abhitemp/
call gcloud dataproc clusters create demo-data-proc --num-workers 2 --image-version 1.0 --zone us-central1-f
call gsutil rm -r gs://abhitemp/bor_predictions
call gcloud dataproc jobs submit pyspark --cluster demo-data-proc --properties spark.jars.packages=com.databricks:spark-csv_2.11:1.2.0 gs://abhitemp/mlspark.py
echo y|gcloud dataproc clusters delete demo-data-proc
call bq load --skip_leading_rows=1 --replace=true --autodetect datalake.dataproc_abhishek gs://abhitemp/bor_predictions/part-00000