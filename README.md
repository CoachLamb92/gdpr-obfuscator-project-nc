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

### Download Repo

- On the repo page, click **<> Code** and select **Download ZIP** from the drop-down menu
- Find the downloaded ZIP in your files
- Extract it
- Open the CLI
- Navigate to the downloaded repo (present working directory should end in: **gdpr-obfuscator-project-nc-main**)
- Run the following commands in the CLI:
  ```
  make create-environment
  make requirements
  make run-checks
  ```
- Check the contents of the **checking_files** folder using the code snippet below:
  ```
  ls testing_files
  ```
- Nothing should be printed to the CLI, as the folder should be empy
- Next, run the following code:
  ```
  make showcase
  ```
- Now, when you execute `ls testing_files`, you should see a file called "test_data_obfuscated.csv"
- Opening it will show a small data set where the personal identifying information has been obfuscated.
- The original data set can be found in the **testing_files** folder under the name: "test_data.csv"
- Execute:

  ```
  cat testing_files/test_data.csv
  ```

  and

  ```
  cat checking_files/test_data_obfuscated.csv
  ```

  to see the differences for yourself!

- If you're tech-savvy enough, open the "showcase_project.py" and change line 7 to:

  ```
  file_name = "gold_price_data.csv"
  ```

  then save the file.
  Repeating the `make showcase` command will obfuscate the data in the "gold_data_price.csv" file, which can be viewed in a similar fashion to the "test_data.csv"

- If you want to use the file with your own data, ensure that the data is saved in a .csv file format in the **testing_files** folder.
- Next, replace the file_name on line 7, and enter the names of the fields you'd like to obfuscate between the square brackets **[ ]** on line 15, with each field name surround in double quotes **" "** and separated by commas **,**
- Use lines 11 and 13 as examples if needed
- Then, just save the file, execute the `make showcase` command, and your file will have it's chosen fields obfuscated!
