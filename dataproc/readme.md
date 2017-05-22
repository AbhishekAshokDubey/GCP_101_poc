gcloud dataproc clusters create abhi-data-proc

gcloud dataproc clusters update abhi-data-proc --num-workers 3

gcloud dataproc clusters create abhi-data-proc --image-version 1.0

gcloud dataproc jobs submit spark --cluster abhi-data-proc --class com.demo.Hello --jars gs://abhitemp/hello_2.12-1.0.jar

gcloud dataproc jobs submit pyspark --cluster abhi-data-proc samplepyspark.py

gcloud dataproc jobs submit pyspark --cluster abhi-data-proc --properties spark.jars.packages=com.databricks:spark-csv_2.11:1.2.0 samplepyspark.py

gcloud dataproc jobs submit pyspark --cluster cluster-14 --properties spark.jars.packages=com.databricks:spark-csv_2.11:1.2.0 gs://abhitemp/mlspark.py

gcloud dataproc clusters delete abhi-data-proc


<br/>
https://cloud.google.com/dataproc/docs/concepts/versioning<br/>
gcloud dataproc jobs submit spark --cluster abhi-data-proc --class org.apache.spark.examples.SparkPi --jars file:///usr/lib/spark/examples/jars/spark-examples.jar 1000