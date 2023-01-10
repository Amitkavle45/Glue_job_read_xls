# Glue_job_read_xls


Excel read is possible in glue version 2 not in glue version 3.  

* Steps:  

## Go to glue job and edit script with below code  
code:   
## 
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


excel_path= r"s3://saama_exercise/infy_input/INFY.xls"  
df_xl_op = pd.read_excel(excel_path,sheet_name = "Sheet1")  
df=df_xl_op.applymap(str)  
input_df = spark.createDataFrame(df)  
input_df.printSchema()  

job.commit()  
Save script  

## Goto Action - Edit Job - Select Glue version2 and set key value under security configuration

 key : --additional-python-modules   
 value : pandas==1.2.4,xlrd==1.2.0,numpy==1.20.1,fsspec==0.7.4    

Save and run the job

## To write the above dataFrame at S3 location
* Include the below code in the script :-
input_df.write.format('csv').option('inferSchema','true').option('header','true').save('s3://ttests/saama_exercise/output_infy/')

* To write the above dataFrame in single partition at S3 location :-
input_df.coalesce(1).write.format('csv').option('inferSchema','true').option('header','true').save('s3://ttests/saama_exercise/output_infy/')

