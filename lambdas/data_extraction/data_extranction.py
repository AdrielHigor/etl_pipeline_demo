import boto3
import json
import os
from datetime import datetime
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import uuid

boto3.setup_default_session(profile_name="etl-demo")

s3 = boto3.client("s3")
sqs = boto3.client("sqs")

TEMP_BUCKET = os.environ.get("TEMP_BUCKET", "temp-recipes-bucket")
FAILED_BUCKET = os.environ.get("FAILED_BUCKET", "failed-recipes-bucket")
QUEUE_URL = os.environ.get("PROCESSING_QUEUE_URL", "recipe-processing-queue")
BATCH_SIZE = os.environ.get("BATCH_SIZE", 100)
MAX_WORKERS = os.environ.get("MAX_WORKERS", 10)


def validate_raw_data(recipe) -> bool:
    required_fields = ["title", "ingredients", "directions"]
    return all(field in recipe for field in required_fields)


def create_s3_bucket_key() -> str:
    date_path = datetime.now().strftime("%Y/%m/%d")
    file_name = f"{uuid.uuid4()}.parquet"

    return f"{date_path}/{file_name}"


def create_temp_file(recipes: list, bucket_name: str) -> str:
    temp_key = create_s3_bucket_key()

    print(f"Creating temp file for {bucket_name} at {temp_key}")
    os.makedirs(os.path.dirname(temp_key), exist_ok=True)

    df = pd.DataFrame(recipes)
    df.to_parquet(temp_key)
    s3.upload_file(temp_key, bucket_name, temp_key)

    os.remove(temp_key)
    return temp_key


def send_message_to_queue(temp_key: str) -> dict:
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(
            {
                "source_bucket": TEMP_BUCKET,
                "source_key": temp_key,
                "timestamp": datetime.now().isoformat(),
            }
        ),
    )

    return response


def extract_recipe_data(recipes) -> str:
    try:
        valid_recipes = []
        invalid_recipes = []

        for recipe in recipes:
            if validate_raw_data(recipe):
                valid_recipes.append(recipe)
            else:
                invalid_recipes.append(recipe)

        temp_key = create_temp_file(valid_recipes, TEMP_BUCKET)

        if invalid_recipes and len(invalid_recipes) > 0:
            failed_key = create_temp_file(invalid_recipes, FAILED_BUCKET)

            if failed_key:
                print(f"Failed recipes saved to {failed_key}")

        response = send_message_to_queue(temp_key)

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            print(f"Error sending message to queue for {temp_key}: {response}")

        return temp_key
    except Exception as e:
        print(f"Error extracting recipe data: {e}")
        return None


def threaded_extraction(batches):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        return list(executor.map(extract_recipe_data, batches))


def lambda_handler(event, context):
    # Extraction Lambda - Focused on raw data ingestion and validation

    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Read raw json data from s3
        raw_data = s3.get_object(Bucket=bucket, Key=key)

        recipes = json.load(raw_data["Body"])

        batches = [
            recipes[i : i + BATCH_SIZE] for i in range(0, len(recipes), BATCH_SIZE)
        ]

        results = threaded_extraction(batches)

        none_results = [result for result in results if result is None]

        if results:
            print(
                f"A total of {len(recipes)} recipes were extracted in {len(results)} batches with {len(none_results)} failed batches"
            )

    return {"statusCode": 200, "body": json.dumps("Data ingestion complete")}


if __name__ == "__main__":
    # Test extraction lambda
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "raw-recipes-data"},
                    "object": {"key": "test_recipes.json"},
                }
            }
        ]
    }

    print(lambda_handler(event, None))
