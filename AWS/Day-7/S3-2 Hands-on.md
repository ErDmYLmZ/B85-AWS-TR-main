
# Hands-on S3 Lifecycle Management and Bucket Replication

Purpose of the this hands-on training is to review how to to create a S3 bucket, configure S3 to host static website, manage lifecycle of objects and to implement bucket replication.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- create a S3 bucket.

- manage lifecycle of objects in S3.

- deploy static Website on S3.

- manage IAM role for bucket replication.

- set the S3 bucket replica.

## Outline

- Part 1 - Creating Bucket for Lifecycle Management and setting Lifecycle Management

- Part 2 - Creating Source and Destination S3 Bucket

- Part 3 - Creating IAM Role for Bucket Replication

- Part 4 - Configuring (Entire) Bucket Replica

- Part 5 - Configuring (Tags, Prefix) Bucket Replica


## Part 1 - Creating S3 Bucket for Lifecycle Management and setting Lifecycle Management


- Create a new bucket named `s3lifecycle.<name>` with following properties.

```text
Allow all public access   : UNCHECKED(PUBLIC) and Acknowledge the warning. 
Versioning                : ENABLE
Tagging                   : 0 Tags
Default encryption        : None
Object lock               : Disabled
```

- Click the S3 bucket `s3lifecycle.<name>` and select following files to upload.

```text
index.html
eagle.jpg
```
- Before clicking upload, create tags for the files. Key: Department Value: Dev After that click upload.

- Create new folders as "lifecylefolder"

- Open lifecycle display of the log bucket from the management tab and add lifecycle rule with following configuration.
```
MANAGEMENT>>>LIFECYCLE>>>>>ADD LIFECYCLE RULE
```

```text
1. Name and scope
Rule Name : life-cycle-rule
Select "Apply to all objects in the bucket"
(Show that you can also select prefix as "lifecyclefolder" but skip it for now)
```

```text
2. Transitions
Select current Version
Click Add transition
Object creation:
    transition to "intelligent tiering after" ---> Days after creation "30" days
```

```text
3. Expiration
Click the current version
Show 365+30=395 (determined 30 days in former page)
```

```text
4. Review
Check the box "I acknowledge that this lifecycle rule will apply to all objects in the bucket."
Click save
```


## Part 2 - Creating Source and Destination S3 Bucket

### Step 1 - Create Source Bucket with Static Website

- Open S3 Service from AWS Management Console.

- Create a bucket of `source.replica.<name>` with following properties,

```text
Region                      : us east-1 (N.Virginia)
Block all public access     : UNCHECKED (PUBLIC)
Versioning                  : ***ENABLE***
Tagging                     : 0 Tags
Default encryption          : Disabled
Object lock                 : Disabled

PS: Please, do not forget to select "US East (N.Virginia)" as Region
```

- Click the S3 bucket `source.replica.<name>` and upload following files.

```text
index.html
eagle.jpg
```

- Click `Properties` >> `Static Website Hosting` and put checkmark to `Use this bucket to host a website` and enter `index.html` as default file.


- Set the static website bucket policy as shown below (`PERMISSIONS` >> `BUCKET POLICY`) and change `bucket-name` with your own bucket.

```json
{
   "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
             "Principal": "*",
             "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::source.replica.yourname/*"
        }
     ]
}
```

- Open static website URL in browser and show it is working.

### Step 2 - Create Destination Bucket

- Create a new bucket named `destination.cross.region.replica.<name>` with following properties.

```text
Region                    : us-east-2 (**Ohio)
Allow all public access   : UNCHECKED (PUBLIC)
Versioning                : ***ENABLED***
Tagging                   : 0 Tags
Default encryption        : Disabled
Object lock               : Disabled


PS: Please, do not forget to select "US East (Ohio)" as Region
```

- Click `Properties` >> `Static Web Hosting` and put checkmark to `Use this bucket to host a website` and enter `index.html` as default file.

- Set the static website bucket policy as shown below (`PERMISSIONS` >> `BUCKET POLICY`) and change `bucket-name` with your own bucket..

```json
{
   "Version":"2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
             "Principal": "*",
             "Action": "s3:GetObject",
            "Resource": "your-resource-name/*"
        }
     ]
}
```

## Part 3 - Creating IAM Role for Bucket Replication

- Go to `IAM Service` on AWS management console.

- Click `Policy` on left-hand menu and select `create policy`.

- Select `JSON` option and paste the policy seen below.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:Get*", 
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::source.replica.<name>(change me)",
                "arn:aws:s3:::source.replica.<name>(change me)/*"
            ]
        },
        {
            "Action": [ 
                "s3:ReplicateObject", 
                "s3:ReplicateDelete",
                "s3:ReplicateTags",
                "s3:GetObjectVersionTagging"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:s3:::destination.cross.region.replica.<name>(change me)/*"
        }
    ]
}
```

- Enter the followings as policy name and description.

```text
Name            : yourname.cross.replication.iam.policy

Description     : yourname.cross.replication.iam.policy
```

- Click `create policy`.

- Go to `Roles` on the left hand menu and click `create role`.

```text
Type of Trusted Entity      : AWS Service
Use Case                    : S3
```

- Click next.

- Enter `yourname.cross.replication.iam.policy` in filter policies box and select the policy

- Click Next `Tag`

```text
Keep it as default
```

- Click Next:Review

- Enter the followings as role name and description an review

```text
Role Name           : yourname.cross.replication.iam.role
Role Description    : yourname.cross.replication.iam.role
```

- Click `create role`.

## Part 4 - Configuring (Entire) Bucket Replica

### Step 1 - Configuring Bucket

- Go to S3 bucket on AWS Console.

- Select `source.replica.<yourname>`.

- Select `Management` >>`Replication Rules` >> `Create Replication Rule`

```text

1. Replication Rule Name:           : MyReplicationRule
2. Status                           : Enable
3. Source Bucket                    : 
   - Choose a rule scope as "This rule applies to all objects in the bucket"
4. Destination                      : 
   - Choose a bucket in this account
   - Bucket name : destination.cross.region.replica.<name>
5. IAM role                         : yourname.cross.replication.iam.role
6. Encryption                       : Unchecked
7. Destination Storage Class        : Unchecked
8. Additional REplication options   : Leave it as is
```

### Step 2 - Testing (Entire)

- Go to VS Code and change the line in `index.html` as;

```html
        <center><h1> The Bald Eagle </h1><center>
                |          |         |
                |          |         |
                V          V         V
        <center><h1> My The Bald Eagle Version 2 </h1><center>

```

- Go to `source.replica.<name>` bucket and upload `index.html` and `eagle.jpg` again.

- Go to `destination.cross.region.replica.<name>` bucket, copy `Endpoint` and paste to browser.

- Show the website is replicated from source bucket.

## Part 5 - Configuring (Tag and Prefix) Bucket Replica

### Step 1 - Configuring with Prefix

- Go to S3 bucket on AWS Console

- Select `source.replica.<name>`.

- Create a folder named `wild`.

- Select `Management` >> `Replication rules` >> `Create replication rule`

```text
a. Replication Rule Name:           : Prefixrule
b. Status                           : Enable
c. Source Bucket                    : 
   - Choose a rule scope as "Limit the scope of this rule usingone or more filters"
   - Prefix                         : wild
   - tag                            : keep it as is
d. Destination                      : 
   - Choose a bucket in this account
   - Bucket name : destination.cross.region.replica.<name>
e. IAM role                         : yourname.cross.replication.iam.role
f. Encryption                       : Unchecked
g. check Storage class and select "One zone IA"
g. Destination Storage Class        : Unchecked
h. Additional Replication options   : Leave it as is

Review and click save
```

- Show that there are two rules.

- Select `Replication rules ` >> Select previous rule click `Action` >> `Disable Rule`

### Step 2 - Testing (Prefix)

- Go to `source.replica.<yourname>` bucket and upload `outside_folder.txt`.

- Go to `destination.cross.region.replica.<name>` bucket and show that the`outside_folder.txt` is not replicated in the bucket.

- This time go to `source.replica.<name>` bucket >> `wild` folder and upload `inside_folder.txt`.

- Go to `destination.cross.region.replica.<name>` bucket show that `wild` folder has been replicated automatically due to replication rule and inside the folder there is `inside_folder.txt file`.

### Step 3 - Configuring with tag

- Go to S3 bucket on AWS Console

- Select `source.replica.<name>`.

- Select `Management` >> `Replication rules` >> `Create replication rule`

```text
a. Replication Rule Name:           : Tagrule
b. Status                           : Enable
c. Source Bucket                    : 
   - Choose a rule scope as "Limit the scope of this rule usingone or more filters"
   - Prefix                         : keep it as is
   - tag                            : Key: Name --- Value: eagle
d. Destination                      : 
   - Choose a bucket in this account
   - Bucket name : destination.cross.region.replica.<name>
e. IAM role                         : yourname.cross.replication.iam.role
f. Encryption                       : Unchecked
g. check Storage class and select "One zone IA"
g. Destination Storage Class        : Unchecked
h. Additional Replication options   : Leave it as is

Review and click save
```
- Show that there are three rules and the first created is disabled.

### Step 2 - Testing (Tag)

- Go to `source.replica.<name>` bucket and direct upload `tag_file.txt`.

- Go to `destination.cross.region.replica.<name>` bucket and show that the `tag_file.txt` is not replicated in the bucket.

- This time go to `source.replica.<name>` bucket, and upload the `tag_file.txt` file with tag as `key:name` and `value:eagle`;

```text
1. Select Add files
    - upload tag_file.txt from local

2. Additional upload options
    - Storage class Standart-IA
    - Tags
        Key     : Name
        Value   : eagle
    and click save button
3. Review and upload
```

- Go to `destination.cross.region.replica.<name>` bucket show that the `tag_file.txt` file is replicated.
