if __name__ == "__main__":
    from evaluate import evaluate_s3, evaluate
    import os
    from dotenv import load_dotenv
    load_dotenv('evaluation/.env')


    AWS_REGION = os.getenv('AWS_REGION')
    AWS_BUCKET = os.getenv('AWS_BUCKET')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')


    evaluate_s3(AWS_REGION, AWS_BUCKET, AWS_ACCESS_KEY, AWS_SECRET_KEY)
