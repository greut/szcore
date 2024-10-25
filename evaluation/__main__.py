




if __name__ == "__main__":
    import argparse
    from evaluate import evaluate_s3, evaluate
    import boto3
    import os
    from dotenv import load_dotenv
    load_dotenv('evaluation/.env')
    import pandas as pd
    import glob


    AWS_REGION = os.getenv('AWS_REGION')
    AWS_BUCKET = os.getenv('AWS_BUCKET')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')


    # # Create an S3 client
    # s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)
    # # List objects in the bucket
    # response =s3.list_objects_v2(Bucket=AWS_BUCKET)
    # for obj in response.get('Contents', []):
    #     key = obj['Key']
    #     break
        
    #     if key.endswith('.tsv') and not key.endswith('participants.tsv'):
    #         print(os.path.basename(obj['Key']))
    #         # Get the object from S3
    #         tsv_obj = s3.get_object(Bucket=AWS_BUCKET, Key=key)
            
    #         # Read the content of the file
    #         tsv_content = tsv_obj['Body'].read().decode('utf-8')
            
    #         # Use pandas to read the TSV content
    #         from io import StringIO
    #         df = pd.read_csv(StringIO(tsv_content), sep='\t')
            
    #         # Print the DataFrame
    #         print(df)
    #         break

            


    # parser = argparse.ArgumentParser(
    #     description="Evaluation code to compare annotations from a seizure detection algorithm to ground truth annotations."
    # )
    # parser.add_argument(
    #     "ref", help="Path to the root folder containing the reference annotations.")
    # parser.add_argument(
    #     "hyp", help="Path to the root folder containing the hypothesis annotations.")

    # args = parser.parse_args()
    evaluate_s3(AWS_REGION, AWS_BUCKET, AWS_ACCESS_KEY, AWS_SECRET_KEY)
