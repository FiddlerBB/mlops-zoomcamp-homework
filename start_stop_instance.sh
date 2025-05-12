#!/bin/bash
INSTANCE_NAME="mlops-instance"
INSTANCE_ID=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=$INSTANCE_NAME" --query "Reservations[].Instances[].InstanceId" --output text)
if [ -z "$INSTANCE_ID" ]; then
  echo "Instance with name $INSTANCE_NAME not found."
  exit 1
fi

#Check if instance state
INSTANCE_STATE=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query "Reservations[].Instances[].State.Name" --output text)
if [ "$INSTANCE_STATE" == "running" ]; then
  echo "Instance $INSTANCE_ID is currently running."
else
  echo "Instance $INSTANCE_ID is currently stopped."
fi


ACTION=$1


if [ "$ACTION" == "start" ]; then
  echo "Starting instance $INSTANCE_ID..."
  aws ec2 start-instances --instance-ids $INSTANCE_ID > /dev/null
  sleep 5 # Wait for the instance to start
  PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query "Reservations[].Instances[].PublicIpAddress" --output text)
  echo "Instance $INSTANCE_ID started."
  echo "Public IP: $PUBLIC_IP"


elif [ "$ACTION" == "stop" ]; then
  echo "Stopping instance $INSTANCE_ID..."
  aws ec2 stop-instances --instance-ids $INSTANCE_ID > /dev/null
  echo "Instance $INSTANCE_ID stopped."
else
  echo "Usage: $0 {start|stop}"
  exit 1
fi
