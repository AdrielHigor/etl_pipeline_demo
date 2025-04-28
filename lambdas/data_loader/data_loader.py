import json
import os
import boto3
import psycopg2
import logging
from psycopg2 import extras

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')

def get_connection():
    """Create a connection to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=os.environ.get('RDS_HOST', 'localhost'),
            port=os.environ.get('RDS_PORT', 5432),
            dbname=os.environ.get('RDS_DB_NAME', 'postgres'),
            user=os.environ.get('RDS_USERNAME', 'postgres'),
            password=os.environ.get('RDS_PASSWORD', 'postgres')
        )
        return conn
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        raise e

def create_table_if_not_exists(conn):
    """Create the recipes table if it doesn't exist"""
    schema = os.environ.get('RDS_SCHEMA', 'public')
    table = os.environ.get('RDS_TABLE', 'recipes')
    
    try:
        with conn.cursor() as cur:
            # Check if schema exists, if not create it
            cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
            
            # Create table if it doesn't exist
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                recipe_id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                difficulty VARCHAR(50),
                prep_time INTEGER,
                cook_time INTEGER,
                servings INTEGER,
                ingredients JSONB,
                instructions JSONB,
                tags JSONB,
                nutrition_info JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()
            logger.info(f"Table {schema}.{table} is ready")
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        conn.rollback()
        raise e

def load_data_to_postgres(conn, data, schema, table):
    """Load the recipe data to PostgreSQL"""
    try:
        with conn.cursor() as cur:
            # Prepare the insert/update query (upsert)
            insert_query = f"""
            INSERT INTO {schema}.{table} (
                recipe_id, name, description, difficulty, prep_time, 
                cook_time, servings, ingredients, instructions, 
                tags, nutrition_info, updated_at
            ) VALUES %s
            ON CONFLICT (recipe_id) 
            DO UPDATE SET 
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                difficulty = EXCLUDED.difficulty,
                prep_time = EXCLUDED.prep_time,
                cook_time = EXCLUDED.cook_time,
                servings = EXCLUDED.servings,
                ingredients = EXCLUDED.ingredients,
                instructions = EXCLUDED.instructions,
                tags = EXCLUDED.tags,
                nutrition_info = EXCLUDED.nutrition_info,
                updated_at = CURRENT_TIMESTAMP
            """
            
            # Prepare the values
            values = []
            for recipe in data:
                values.append((
                    recipe.get('recipe_id'),
                    recipe.get('name'),
                    recipe.get('description'),
                    recipe.get('difficulty'),
                    recipe.get('prep_time'),
                    recipe.get('cook_time'),
                    recipe.get('servings'),
                    json.dumps(recipe.get('ingredients', [])),
                    json.dumps(recipe.get('instructions', [])),
                    json.dumps(recipe.get('tags', [])),
                    json.dumps(recipe.get('nutrition_info', {})),
                    'CURRENT_TIMESTAMP'
                ))
            
            # Execute the query
            extras.execute_values(cur, insert_query, values)
            conn.commit()
            logger.info(f"Successfully loaded {len(values)} recipes to PostgreSQL")
    except Exception as e:
        logger.error(f"Error loading data to PostgreSQL: {e}")
        conn.rollback()
        raise e

def lambda_handler(event, context):
    """Lambda handler for loading processed data to PostgreSQL"""
    try:
        # Get S3 bucket and object key from the event
        logger.info(f"Processing event: {json.dumps(event)}")
        
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            logger.info(f"Processing file {key} from bucket {bucket}")
            
            # Get the object from S3
            response = s3_client.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read().decode('utf-8')
            data = json.loads(content)
            
            # Connect to PostgreSQL
            conn = get_connection()
            
            # Create table if it doesn't exist
            schema = os.environ.get('RDS_SCHEMA', 'public')
            table = os.environ.get('RDS_TABLE', 'recipes')
            create_table_if_not_exists(conn)
            
            # Load data to PostgreSQL
            load_data_to_postgres(conn, data, schema, table)
            
            # Close the connection
            conn.close()
            
            logger.info(f"Successfully processed file {key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data loaded successfully to PostgreSQL')
        }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error loading data: {str(e)}')
        }

if __name__ == "__main__":
    # For local testing
    test_event = {
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': 'processed-recipes-bucket'
                    },
                    'object': {
                        'key': 'test-recipe.json'
                    }
                }
            }
        ]
    }
    lambda_handler(test_event, {})