import boto3
import pandas as pd
import os
import re
import io
from datetime import datetime
import uuid

boto3.setup_default_session(profile_name="etl-demo")

s3 = boto3.client("s3")

PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "processed-recipes-bucket")

TIME_UNITS = {
    "hours": 3600,
    "hour": 3600,
    "minutes": 60,
    "minute": 60,
    "seconds": 1,
    "second": 1,
}


def get_complexity_score(ingredients: list, directions: list) -> int:
    return (len(directions) * 0.6) + (len(ingredients) * 0.4)


def get_difficulty_flag(complexity_score: int) -> str:
    if complexity_score < 4:
        return "easy"
    elif complexity_score < 8:
        return "medium"
    else:
        return "hard"


def get_recipe_id() -> str:
    return str(uuid.uuid4())


def get_time_estimate(directions: list) -> int:
    time_estimate = 0

    # Pattern to identify time units in the directions first find the number and the next word after the number
    time_pattern = re.compile(r"(\d+)\s*(\w+)")

    for direction in directions:
        matches = time_pattern.findall(direction)

        any_match = False
        for match in matches:
            number = match[0]
            unit = match[1]

            if unit not in TIME_UNITS:
                continue

            time_estimate += int(number) * TIME_UNITS[unit]
            any_match = True

        if not any_match:
            # Estimate 5 minutes if no time units are found
            time_estimate += 300

    return time_estimate


def transform_row(row: pd.Series) -> pd.Series:
    row["complexity_score"] = get_complexity_score(
        row["ingredients"], row["directions"]
    )
    row["difficulty_flag"] = get_difficulty_flag(row["complexity_score"])
    row["time_estimate"] = get_time_estimate(row["directions"])
    row["recipe_id"] = get_recipe_id()

    return row


def lambda_handler(event, context):
    # Transformation Lambda - Focused on data processing
    for record in event["Records"]:
        temp_bucket = record["source_bucket"]
        temp_key = record["source_key"]

        print(f"Processing file from {temp_bucket}/{temp_key}")

        # Read temporary Parquet file
        temp_file = s3.get_object(Bucket=temp_bucket, Key=temp_key)

        print(temp_file)

        buffer = io.BytesIO(temp_file["Body"].read())
        df = pd.read_parquet(buffer)

        # Data transformations
        df = df.apply(transform_row, axis=1)

        # Save only the columns we need
        df = df[
            [
                "title",
                "ingredients",
                "directions",
                "tags",
                "complexity_score",
                "difficulty_flag",
                "time_estimate",
                "recipe_id",
            ]
        ]

        # Save to processed storage
        output_key = f"{df['difficulty_flag']}/{temp_key.split('/')[-1]}"

        # Save to processed storage
        s3.put_object(Bucket=PROCESSED_BUCKET, Key=output_key, Body=df.to_parquet())

    return {"statusCode": 200}


if __name__ == "__main__":
    # Test transformation lambda
    event = {
        "Records": [
            {
                "source_bucket": "temp-recipes-bucket",
                "source_key": "2025/02/17/7c9e82bd-9ed4-44d0-a9a0-8215b23eb3ad.parquet",
                "timestamp": "2024-01-01T00:00:00Z",
            }
        ]
    }

    print(lambda_handler(event, None))
