# GDPR Obfuscator

## Summary

BLAH BLAH BLAH

## Putting the Obfuscator in an AWS Lambda

### Download Repo

- On the repo page, click <> Code and select Download ZIP from the drop-down menu
- Find the downloaded ZIP in your files
- Extract it

### Set Up Bucket

- Create an AWS account
- Navigate to the S3 page
- Navigate to General purpose buckets page in the left-hand menu
- Click Create bucket
- Name the bucket
- Scroll down and click Create bucket
- Navigate back to General purpose buckets and select the bucket you just created
- Click Upload
- Click Add files
- Select FILENAME from this downloaded repo
- Click Upload
- Click Close

### Set Up Permissions

- Navigate to IAM
- Navigate to Roles on left-hand menu
- Click Create role
- Choose Lambda from the drop-down menu in the Use case window
- Click Next
- Select AmazonS3FullAccess from the Permissions Policies
- Click Next
- Name your role
- Click Create role

### Set Up Lambda

- Navigate to Lambda page
- Create function
- Name function
- Change runtime to Python 3.13 from drop-down menu
- Click Create function
- Scroll down to code source window
- Select .zip file from Upload from drop-down menu
- Click Upload
- Select FILENAME.zip from this downloaded repo
- Click Upload

<b>Add Permissions</b>

- Navigate to Configurations tab
- Navigate to Permissions on left-hand menu
- Click Edit in Execution role window
- Select the role you created from the Existing role drop-down menu

<b>Test Lambda</b>

- Navigate to Test tab
- Name the test
- Replace the text in Event JSON box with the following:

```
{
    "file_to_obfuscate": "s3://<your_bucket_name>/FILENAME",
    "pii_fields": ["name", "email_address"]
}
```

where **<your_bucket_name>** is replaced by the name of the bucket you just made

- Click Save
- Click test
- Navigate back to S3 page
- Click on the bucket you made
- You should see a new file named PILENAME_obfuscated.csv
- Upon opening it, you should see the fields "name" and "email_address" are obfuscated

## Using the Obfuscator locally
