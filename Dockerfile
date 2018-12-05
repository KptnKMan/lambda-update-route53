# python image for build
FROM python:2.7.14-alpine

# copy python requirements into image and run
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy my app into image
COPY code_local/update_route53.py ./

# setup my variables
ENV AWS_DOMAIN=None
ENV IP=None
ENV CHECK_URL="http://api.ipify.org"
ENV AWS_ACCESS_KEY_ID=None
ENV AWS_SECRET_ACCESS_KEY=None
ENV AWS_REGION_NAME="eu-west-1"
ENV AWS_STREAM_NAME="lambda-update-route53"
ENV AWS_PARTITION_KEY="shardId-000000000000"

# run my application
CMD python ./update_route53.py \
--aws_domain $AWS_DOMAIN \
--ip $IP \
--check_url $CHECK_URL \
--aws_key $AWS_ACCESS_KEY_ID \
--aws_secret $AWS_SECRET_ACCESS_KEY \
--aws_region $AWS_REGION_NAME \
--aws_stream_name $AWS_STREAM_NAME \
--aws_partition_key $AWS_PARTITION_KEY
