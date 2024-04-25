# Setting Up an S3 Static Website Using AWS CLI

## Introduction

In this hands-on lab, we'll be setting up an S3 bucket website. We'll also verify the website is accessible and working as expected. S3 bucket websites are excellent for hosting single-page, customer-facing content, as they are easy to set up and offer the same high availability and scalability as S3.

1. Open a terminal session and log in to the provided EC2 instance via SSH using the credentials provided on the lab page:

```bash
ssh cloud_user@<PUBLIC IP>
```

2. Create an S3 Bucket from AWS CLI 

- Create an S3 bucket in the us-east-1 region, replacing <UNIQUE_BUCKET_NAME> with a unique bucket name, and using the S3 API:

```bash
aws s3api create-bucket --bucket <UNIQUE_BUCKET_NAME> --acl public-read
```

3. Modify the Newly Created Bucket to Be an S3 Website Bucket

- Issue the AWS S3 API CLI command to enable the "Static website hosting" property of your bucket. In this same command, you'll also provide the index.html page, which is what your bucket URL will serve:

```bash
aws s3 website s3://<UNIQUE_BUCKET_NAME> --index-document index.html
```
4. Modify Provided S3 Policy File and Use It to Modify the Bucket Policy

- Open the policy_s3.json file:

```bash
vim policy_s3.json
```
- copy the json file content in it.


```json
{
   "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
             "Principal": "*",
             "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<UNIQUE_BUCKET_NAME>/*"
        }
     ]
}
```

- Save and exit the file.

5. Use the S3 policy file to modify the bucket policy so your objects are publicly accessible, which is a requirement for S3 static websites:

```bash
aws s3api put-bucket-policy --bucket <UNIQUE_BUCKET_NAME> --policy file://policy_s3.json
```

6. Clone our web site from github Page and Upload File to S3 Website Bucket

```bash
sudo apt-get install git
git clone https://github.com/techproedu/designer.git
cd designer
```

6. Upload the all files to your S3 website bucket:

```bash
aws s3 cp ./ s3://<UNIQUE_BUCKET_NAME> --recursive
```

7. Verify Your S3 Static Website Is Working

- Enter the S3 website URL for your bucket in the browser to ensure it's working.
- `S3 Buckets > <youruniquebucketname> > Properties > Static Website Hosting > Bucket Website Endpoint`
8. To delete all the objects from an S3 bucket, --recursive option can be used after the specified bucket name as shown below.

```bash
aws s3 rm s3://bucket-name --recursive
```
9. To delete the bucket give command shown below.

```bash
aws s3 rb s3://bucket-name
``` 
10. Instead of 8th and 9th step you can force to delete, so you can imply that command shown below

```bash
aws s3 rm s3://bucket-name --recursive --force
```

Congratulations on successfully completing this hands-on lab!