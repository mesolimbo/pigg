# pigg

Python Idea Generator Generator.

## Create Deployment Package

```bash
pipenv lock -r > requirements.txt
mkdir package
cd package
pipenv run pip install -r ../requirements.txt -t .
cp -r ../pigg .
zip -r ../my_deployment_package.zip .
cd ..
```

## Upload and Configure the Lambda Function

1. Create a Lambda function using the AWS Management Console or AWS CLI. 
2. Upload the Deployment Package:
   In the AWS Management Console, upload my_deployment_package.zip to your Lambda function.
3. Set the Handler:
   Set the handler to pigg.lambda_function.lambda_handler.
4. Configure IAM Role:
    Ensure the Lambda function has an IAM role with permissions to access the specified S3 bucket.

## Generate the Markov Chain JSON

Run the generate_markov_chain.py script locally to generate the markov_chain.json file:

```bash
pipenv run python generate_markov_chain.py data/printables.csv chains/printables_chain.json
```

Upload the generated markov_chain.json file to your S3 bucket.

## Test the Lambda Function

Invoke the Lambda function with a test event:

```json
{
  "bucket_name": "your-bucket-name",
  "file_key": "markov_chain.json",
  "n_sentences": 5
}
```
