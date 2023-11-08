
import boto3
import json
import sys

input_filename = sys.argv[1]
with open(input_filename, "r", encoding="utf-8") as input_file:
    env = json.load(input_file)
print(env) # Dictionaire contenant le json d'entrée

session = boto3.Session()
s3 = session.client("s3",region_name=env["Location"])
Lambda = session.client("lambda",region_name=env["Location"])

try :
    response = s3.head_bucket(
        Bucket=env["NomBucket"],
        
        
)
    ## print(response)
except :
     
     s3.create_bucket(
    
    Bucket=env["NomBucket"],
    CreateBucketConfiguration={
        'LocationConstraint':env["Location"]
    },
    
)

response = s3.put_bucket_tagging(
    Bucket=env["NomBucket"],
    Tagging={
        'TagSet': [
            {
                'Key': 'school',
                'Value': 'esgi',
            },
            {
                'Key': 'promotion',
                'Value': 'al-m2',
            },
            {
                'Key': 'user',
                'Value': 'TheoAzouz',
            },
        ],
    },
)

response = s3.upload_file(env["FichierZip"], env["NomBucket"], env["FichierZip"])


print(response)

response = Lambda.create_function(
    Code={
        'S3Bucket': env["NomBucket"],
        'S3Key': env["FichierZip"],
    },
    Description='Process image objects from Amazon S3.',
    Environment={
        'Variables': {
            'BUCKET': 'my-bucket-1xpuxmplzrlbh',
            'PREFIX': 'inbound',
        },
    },
    FunctionName=env["NomFonction"],
    Handler='lambda_function.lambda_handler',
    Role=env["NomRole"],
    Runtime='python3.10',
    Tags={
        'school': 'esgi',
        'promotion':'al-m2',
        'user' : 'TheoAzouz'
    },

)

print(response)