# GDPR Obfuscator

## Summary

BLAH BLAH BLAH

## Putting the Obfuscator in an AWS Lambda

### Download Repo

- On the repo page, click **<> Code** and select **Download ZIP** from the drop-down menu
- Find the downloaded ZIP in your files
- Extract it

### Set Up Bucket

- Create an AWS account
- Navigate to the S3 page
- Navigate to **General purpose buckets** page in the left-hand menu
- Click **Create bucket**
- Name the bucket
- Scroll down and click **Create bucket**
- Navigate back to **General purpose buckets** and select the bucket you just created
- Click **Upload**
- Click **Add files**
- Select **test_data.csv** from the **testing_files** folder in the downloaded repo
- Click **Upload**
- Click **Close**

### Set Up Permissions

- Navigate to IAM
- Navigate to **Roles** on left-hand menu
- Click **Create role**
- Choose **Lambda** from the drop-down menu in the **Use case** window
- Click **Next**
- Choose **AmazonS3FullAccess** from the **Permissions Policies**
- Click **Next**
- Name your role
- Click **Create role**

### Set Up Lambda

- Navigate to Lambda page
- Click **Create function**
- Name function
- Select **Python 3.13** from the **run-time** drop-down menu
- Click **Create function**
- Scroll down to **code source** window
- Select **.zip file** from the **Upload** drop-down menu
- Click **Upload**
- Select **gdpr-lambda.zip** from this downloaded repo
- Click **Save**

<b>Add Permissions</b>

- Navigate to **Configurations** tab
- Navigate to **Permissions** on left-hand menu
- Click **Edit** in the **Execution role** window
- Select the role you created from the **Existing role** drop-down menu
- Click **Save**

<b>Test Lambda</b>

- Navigate to **Test** tab
- Name the Event
- Replace the text in **Event JSON** box with the following:

```
{
    "file_to_obfuscate": "s3://<your_bucket_name>/test_data.csv",
    "pii_fields": ["name", "email_address"]
}
```

- Replace **<your_bucket_name>** in the **Event JSON** box with the name of the bucket you just made

- Click **Save**
- Click **Test**
- If the execution fails, wait 20 seconds and click **Test** again
- Navigate back to S3 page
- Click on the bucket you made
- You should see a new file named **test_data_obfuscated.csv**
- Upon opening it, you should see the fields "name" and "email_address" are obfuscated

## Using the Obfuscator locally
