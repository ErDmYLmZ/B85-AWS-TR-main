# Hands-on S3-01 : S3 Website Hosting, Versioning and Logging

Purpose of this hands-on training is to instruct students how to create a S3 bucket, how to configure S3 to host static website and to give understanding of versioning and logging.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- create a S3 bucket,

- upload and customize files to S3 bucket,

- deploy static Website on S3,

- set the S3 bucket policies,

- configure S3 bucket with versioning options,

- monitor logging records,


## Outline

- Part 1 - S3 Bucket Basic Operations

- Part 2 - Creating a new Bucket for Static Website

- Part 3 - Creating S3 Bucket with Versioning

- Part 4 - Logging

## Part 1 - S3 Bucket Basic Operations

- Open S3 Service from AWS Management Console.

- Create a bucket with following properties,

```text
Bucket name                 : myfirstbucket-yourname
Region                      : N.Virginia
Block all public access     : Checked (KEEP BlOCKED)
Versioning                  : Disabled
Tagging                     : 0 Tags
Default encryption          : None
Object-level logging        : Disabled

```

- Explain;

  - Naming convention (unique, global),

  - Why we choose region,

  - Redundancy,

  - Availability.

- Upload files in `S3-files` folder.

- Show the file details.

- Open one of the file's URL in the browser and show that it is not accessible.

- Open the file using pre-signed URL in the browser and show that it is accessible for a short time.

- Try to make the object public, face with `Error Access denied`.

- Open the bucket permissions, change it to public:

```
PERMISSIONS >> BLOCK PUBLIC ACCESS>>>> EDIT>>> UNCHECKED
```

- Check in the main Bucket Page, if Access property of your listed bucket appears to be `Objects can be public`

- Go and select one of the files uploaded in the bucket and see if you can view it on a browser like public. If you can not see it, it is still private.

- Go back to your bucket view and click Permissions. Edit Object Ownership. Select ACLs enabled and save changes.

- Got to one of the objects/files, select and select Make Public using ACL from Object actions.

- Open the file URL in the browser, show it is accessible now.

- Create a folder named it as 'images', explain why a folder is also called as prefix in S3

- Move one of the files into the folder.

- Open the file URL in the browser and show that it is "Not Accessible."

- Select the folder and make it "Public".

- Open the file URL in the browser, show it is accessible now.

- Show how to delete any object.

```text
delete ---> logo.png
```

- Show how to rename `S3.png file.

```text
rename S3.png as S3_renamed.png
```

- Show how to delete the folder,

```text
delete ---> folder1
```

- Show that it is deleted even if there are objects in folder.

- Upload a file into the S3 Bucket (without drag and drop) and navigate to advanced step `Set permissions` part and explain the storage classes (S3 Standard, Standard IA, Glacier: 3 AZs, Durability 11/9)

## Part 2 - Creating a new Bucket for Static Website


- Create a new bucket for website logging with name of `log.myname.bucket.website` and with following properties.

```text
Bucket name                 : log.myname.bucket.website
Region                      : N.Virginia
Block all public access     : Checked (KEEP BlOCKED)
Versioning                  : Disabled
Tagging                     : 0 Tags
Default encryption          : None
Object-level logging        : Disabled
```
- Create 1 folder named : `staticwebhosting`


- Create a new bucket for static website with name of `myname.bucket.website` and with following properties

```text
Bucket name                 : myname.bucket.website
Region                      : N.Virginia
Block all public access     : Checked (KEEP BlOCKED)
Versioning                  : ENABLED****
Tagging                     : 0 Tags
Default encryption          : None
Object-level logging        : Disabled
```

- Change the Server access logging settings of the `myname.bucket.website`

```text
Go to the "Properties >>>>>>>> Server access logging >>>>>>> EDIT

Server access logging     : ENABLED  (- Target Bucket ---> log.myname.bucket.website)
                                      - Target prefix------>"staticwebhosting"

```

- Click the S3 bucket `myname.bucket.website` and upload freelanceweb contents.

```text
index.html
error.html
assets folder
```

- Show static website hosting settings from properties of `myname.bucket.website` bucket.

```
PROPERTIES>>>>> STATIC WEBSITE HOSTING
```

- Click static web hosting and put check mark to `Use this bucket to host a website` and enter `index.html` as default file, `error.html` as the alternative.

- Copy endpoint and show that the website is Not Accessible.

-  Change the bucket Public Access status from CHECKED(BLOCKED) to UNCHECKED(PUBLIC).

```
PERMISSIONS >> BLOCK PUBLIC ACCESS>>>> EDIT>>> UNCHECKED
```
- Set the static website bucket policy as shown below (PERMISSIONS >> BUCKET POLICY) and change `bucket-name`  with your own bucket.



```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::don't forget to change me/*"
        }
    ]
}
```

- Open static website URL in browser and show its working.



## Part 3 - Creating S3 Bucket with Versioning


- Open the bucket page of static website.

- Show versioning of the files right under the bucket `myname.bucket.website`

- Delete `index.html`.

- Turn the version option `ON` from `List version` tab.

- Show the `index.html` file is still in the bucket.

- Show the `delete marker` below the `index.html` file.

- Delete `delete markers` of the index.html and show that they are available again.

- Open `index.html` from local with VS Code and change the statement as shown below.

```text
<center><h1> Lorem Web Design, Grafik Design ve SEO Hizmetleri</h1><center>
    |             |              |
    |             |              |
    |             |              |
    V             V              V
<center><h1> DevOps Team Web Arayüzü 1 </h1><center>
```

- Upload a new version of the `index.html`.

- Turn the version option `ON` from `List version` tab and see two versions of `index.html`.

- Open static website URL in browser again, observe that it is showing the new content (Version 1).

- Again open `index.html` from local with VS Code and change statement as shown below.

```text
<center><h1> DevOps Team Web Arayüzü 1</h1><center>
    |             |              |
    |             |              |
    |             |              |
    V             V              V
<center><h1> DevOps Team Web Arayüzü 2</h1><center>
```

- Upload the newest version of `index.html` to the bucket.

- Turn the version option `ON` from `List version` tab  and see three versions of `index.html`.

- Open static website URL in browser again, observe that it is showing the new content (Version 2).

- Show versioning of the index.html, and delete the latest version.

- Open static website URL in browser again, observe that it is showing the "Version 1" content.

## Part 4 - Logging

- Open the bucket endpoint in a different device like a mobile phone. Then check the logs.

- Open `log.myname.bucket.website` bucket and show logging of "myname.bucket.website" 
