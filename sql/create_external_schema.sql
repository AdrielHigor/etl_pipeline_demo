-- Create external schema
CREATE EXTERNAL SCHEMA recipes_spectrum
FROM DATA CATALOG 
DATABASE 'recipes_db'
IAM_ROLE 'arn:aws:iam::396913730966:role/RedshiftSpectrumRole'
CREATE EXTERNAL DATABASE IF NOT EXISTS;

-- Create external table
CREATE EXTERNAL TABLE recipes_spectrum.recipes_external (
    title VARCHAR(255),
    ingredients SUPER,
    directions SUPER,
    tags SUPER,
    complexity_score FLOAT,
    difficulty_flag VARCHAR(10),
    time_estimate INTEGER,
    recipe_id VARCHAR(36) PRIMARY KEY
)
PARTITIONED BY (difficulty_flag VARCHAR(10))
STORED AS PARQUET
LOCATION 's3://processed-recipes-bucket/';