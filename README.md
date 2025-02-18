I've been working directly with it and studying it a lot I would like to propose writing on how to build data pipelines with aws lambdas and s3.
The example would be basically:
1 - ingesting raw data from a csv/public api into an s3 bucket/or via api gateway (haven't decided on that yet)
2 - triggering aws lambdas for data extraction
3 - save raw results to temp s3 storage as a Parquet file
4 - trigger lambda to validate and transform the raw data (probably using s3 events or a scheduler)
5 - save processed data to s3 with dynamic partitioning (also parquet files)
6 - Using redshift spectrum to analyze the data directly from S3 using external schemas and SQL queries
