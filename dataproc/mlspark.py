#!/usr/bin/python
import pyspark
sc = pyspark.SparkContext()

# pyspark --packages com.databricks:spark-csv_2.10:1.4.0
# distinct_values_in_each_cat_var = [df.select(x).distinct().count() for x in char_col_toUse_names] 


from pyspark.sql import SQLContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.tree import RandomForest
from pyspark.sql.functions import col

from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder, Tokenizer, HashingTF, VectorIndexer


sqlContext = SQLContext(sc)

df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('gs://abhitemp/Wline_bor_date_header.csv')


char_col_toUse_names = ['sub_geomarket','country','sub_segment','std_job_type','std_service_line','rig_environment','well_type','bhp_range','bit_size_range','customer_name','rig_name','equipment_category']
num_col_toUse_names = ['job_days']
label_col = 'equipment_days'

string_indexers = [
   StringIndexer(inputCol=x, outputCol="int_{0}".format(x))
   for x in char_col_toUse_names
]

encoder = [
   OneHotEncoder(inputCol="int_{0}".format(x), outputCol="one_hot_{0}".format(x))
   for x in char_col_toUse_names
]

assembler = VectorAssembler(
    inputCols= ["one_hot_"+x for x in char_col_toUse_names] + num_col_toUse_names,
    outputCol="features"
)

pipeline = Pipeline(stages = string_indexers + encoder + [assembler])
model = pipeline.fit(df)
indexed = model.transform(df)
ml_df = indexed.select(col(label_col).cast("int").alias("label"), col("features")).map(lambda row: LabeledPoint(row.label, row.features))


training, test = ml_df.randomSplit([0.7, 0.3], seed=0)

gbm = RandomForest.trainRegressor(training, categoricalFeaturesInfo={0:2,1:4,2:2,3:7,4:3,5:4,6:3,7:6,8:4,9:51,10:96,11:34}, numTrees=10, featureSubsetStrategy="auto", impurity='variance', maxDepth=5, maxBins=120)

predictions = gbm.predict(test.map(lambda x: x.features))

labelsAndPredictions = test.map(lambda x: x.label).zip(predictions)

error = 1.0 * labelsAndPredictions.filter(lambda (p, a): a!=0).map(lambda (p, a): abs(p-a)/a).reduce(lambda a, b: a+b) / test.count()
print(".......--------================= Error on test with one hot encoding: "+ str(error))


all_predictions = gbm.predict(ml_df.map(lambda x: x.features))
df_rdd = df.rdd

predictionsDF = df_rdd.zip(all_predictions).toDF(["given","out"])

from pyspark.sql.functions import udf, col
from pyspark.sql.types import FloatType, DoubleType, IntegerType, NullType, StringType

udf_field_ticket = udf(lambda value: str(value[0]), StringType())
udf_area = udf(lambda value: str(value[1]), StringType())
udf_geomarket = udf(lambda value: str(value[2]), StringType())
udf_sub_geomarket = udf(lambda value: str(value[3]), StringType())
udf_country = udf(lambda value: str(value[4]), StringType())
udf_sub_segment = udf(lambda value: str(value[5]), StringType())
udf_std_job_type = udf(lambda value: str(value[6]), StringType())
udf_std_service_line = udf(lambda value: str(value[7]), StringType())
udf_rig_environment = udf(lambda value: str(value[8]), StringType())
udf_well_type = udf(lambda value: str(value[9]), StringType())
udf_bhp_range = udf(lambda value: str(value[10]), StringType())
udf_bit_size_range = udf(lambda value: str(value[11]), StringType())
udf_customer_name = udf(lambda value: str(value[12]), StringType())
udf_rig_name = udf(lambda value: str(value[13]), StringType())
udf_well_name = udf(lambda value: str(value[14]), StringType())
udf_hole_section_id = udf(lambda value: str(value[15]), StringType())
udf_start_date = udf(lambda value: str(value[16]), StringType())
udf_end_date = udf(lambda value: str(value[17]), StringType())
udf_bookingstatus = udf(lambda value: str(value[18]), StringType())
udf_equipment_code = udf(lambda value: str(value[19]), StringType())
udf_equipment_category = udf(lambda value: str(value[20]), StringType())
udf_equipment_group = udf(lambda value: str(value[21]), StringType())
udf_equipment_family = udf(lambda value: str(value[22]), StringType())
udf_job_days = udf(lambda value: str(value[23]), StringType())
udf_equipment_days = udf(lambda value: int(value[24]), IntegerType())

udf_pred_equipment_days = udf(lambda value: float(value), FloatType())

predictionsDF_new = predictionsDF.select(udf_field_ticket('given').alias('field_ticket'),
	udf_area('given').alias('area'),
	udf_geomarket('given').alias('geomarket'),
	udf_sub_geomarket('given').alias('sub_geomarket'),
	udf_country('given').alias('country'),
	udf_sub_segment('given').alias('sub_segment'),
	udf_std_job_type('given').alias('std_job_type'),
	udf_std_service_line('given').alias('std_service_line'),
	udf_rig_environment('given').alias('rig_environment'),
	udf_well_type('given').alias('well_type'),
	udf_bhp_range('given').alias('bhp_range'),
	udf_bit_size_range('given').alias('bit_size_range'),
	udf_customer_name('given').alias('customer_name'),
	udf_rig_name('given').alias('rig_name'),
	udf_well_name('given').alias('well_name'),
	udf_hole_section_id('given').alias('hole_section_id'),
	udf_start_date('given').alias('start_date'),
	udf_end_date('given').alias('end_date'),
	udf_bookingstatus('given').alias('bookingstatus'),
	udf_equipment_code('given').alias('equipment_code'),
	udf_equipment_category('given').alias('equipment_category'),
	udf_equipment_group('given').alias('equipment_group'),
	udf_equipment_family('given').alias('equipment_family'),
	udf_job_days('given').cast('int').alias('job_days'),
	udf_equipment_days('given').cast('int').alias('equipment_days_actual'),
	udf_pred_equipment_days('out').cast('float').alias('equipment_days_predicted')
	)

predictionsDF_new.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").save("gs://abhitemp/bor_predictions")