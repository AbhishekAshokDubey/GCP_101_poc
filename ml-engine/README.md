>gcloud ml-engine jobs submit training task1 --module-name train.second  --package-path train  --staging-bucket gs://abhi-ml --region us-central1 --  --input_dir=gs://abhi-ml/data  --train_files=gs://abhi-ml/data/data.csv --output_dir=gs://abhi-ml/output


Note:
The data file, data.csv, is in the cloud bucket 'gs://abhi-ml/data', inside 'data' folder.