# AWS_Data_Quest

## My submission files
- **S3 data links**: 
        - Json API file: https://rearcdataquest.s3.us-east-2.amazonaws.com/population_data.json
        - Database root: https://rearcdataquest.s3.us-east-2.amazonaws.com/pr/
        - Example of db file: https://rearcdataquest.s3.us-east-2.amazonaws.com/pr/pr.data.0.Current
- **Source code part 1 and 2**: [S3_Datasets_API.py](https://github.com/JMOriggi/Rearc_data_quest/blob/main/S3_Dataset_API.py)
- **Source code part 3**: [Data_Analytics.ipynb](https://github.com/JMOriggi/Rearc_data_quest/blob/main/Data_Analytics.ipynb) 
- **Source code part 4 (using terraform)**: [Data_Pipeline Infrastructure](https://github.com/JMOriggi/Rearc_data_quest/blob/main/Data_Pipeline_Infrastructure/) 


## Comments
This was my first time handling an S3 and Lambda configuration on AWS. I found the assignments very engaging. Some components of the final deployment (part4 only) haven't been completed, since I couldn't debug all the issues in the reasonable time required to complete the assignment (around 4h of work and documentation reading). Overall, I'm satisfied with the results I have achieved. I look forward to hearing your feedback and suggestions on how to fix and improve my implementation.

Missing components: 
- The sqs queue with s3 notifications is not implemented (a problem in creating the "aws_s3_bucket_notification" resource).
- Dependencies for python modules not tested on AWS.
- Exception handling for the python methods.
- Methods and functions comments.
