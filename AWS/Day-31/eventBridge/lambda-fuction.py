# importing modules
import logging
import boto3
import json

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to INFO
logger.setLevel(logging.INFO)

# ASG boto3 client creation
asg_client = boto3.client("autoscaling")

original_desired_capacity = "1"


def lambda_handler(event, context):
    # Parsing incoming event data.
    autoscaling_group_name = event["detail"]["AutoScalingGroupName"]
    event_description = event["detail-type"]

    # logging the event name and ASG name
    logger.info(
        f"We have just received notice that the Autoscaling Group `{autoscaling_group_name}` has just received an {event_description} event."
    )

    # Getting ASG details
    asg_details = asg_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            autoscaling_group_name,
        ],
    )
    asg_environment_tags = asg_details["AutoScalingGroups"][0]["Tags"]
    new_min_size = asg_details["AutoScalingGroups"][0]["MinSize"]
    new_max_size = asg_details["AutoScalingGroups"][0]["MaxSize"]
    new_desired_size = asg_details["AutoScalingGroups"][0]["DesiredCapacity"]

    logger.info(f"Detected desired capacity was set to: {new_desired_size}")
    logger.info(f"Detected min size was set to: {new_min_size}")
    logger.info(f"Detected max size was set to: {new_max_size}")

    # Getting tags of ASG
    asg_tags = asg_client.describe_tags(
        Filters=[
            {"Name": "auto-scaling-group", "Values": [autoscaling_group_name]}
            # {"Name": "k", "Values": [autoscaling_group_name]},
        ]
    )
    # Getting the tag information, and if matching to `prd`, resetting to the original capacity.
    for tag in asg_tags["Tags"]:
        if tag["Key"] == "env":
            if tag["Value"] == "prd":
                logger.info(
                    f"Production autoscaling group detected. Checking updated capacity status."
                )
                if new_desired_size != 1:
                    logger.info(
                        f"Resetting {autoscaling_group_name} to baseline capacity of {original_desired_capacity}."
                    )
                    asg_client.set_desired_capacity(
                        AutoScalingGroupName=autoscaling_group_name,
                        DesiredCapacity=1,
                        HonorCooldown=False,
                    )
            elif tag["Value"] == "dev":
                logger.info(
                    f"Development autoscaling group detected. Not taking any action."
                )
            else:
                logger.warning(
                    f"Required tags not found. Please add them to the {autoscaling_group_name}."
                )
