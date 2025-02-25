def lambda_handler(event, context):
    print(event)
    return {
        "statusCode": 200,
        "body": "Data loaded successfully"
    }

if __name__ == "__main__":
    lambda_handler({}, {})