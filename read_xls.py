import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import pandas as pd

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


excel_path= r"s3://ttests/saama_exercise/infy_input/INFY.xls"
df_xl_op = pd.read_excel(excel_path)
df=df_xl_op.applymap(str)
input_df = spark.createDataFrame(df)
input_df.printSchema()
input_df.show()
'''
df_infy=input_df.toDF(*(re.sub('[^a-zA-Z0-9]','',c) for c in df.columns))

res1 = df_infy.withColumn('Date',to_date('Date','M/d/yyyy'))
res1.show(50)
#res1.printSchema()
'''
input_df.write.format('csv').option('inferSchema','true').option('header','true').save('s3://ttests/saama_exercise/output_infy12/')
job.commit()