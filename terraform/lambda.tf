// AWS IAM role for Lambda Function
resource "aws_iam_role" "iam_role_for_lambda" {
  name = "lambda-update-route53-${var.project_name_short}-lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

// This policy allows Allows Lambda to:
// update route53 and kinesis
// create a log group, log stream, put events into streams
resource "aws_iam_role_policy" "iam_policy_for_lambda" {
  name = "lambda-update-route53-${var.project_name_short}-policy"
  role = "${aws_iam_role.iam_role_for_lambda.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowRoute53AndKinesis",
            "Effect": "Allow",
            "Action": [
                "route53:*",
                "kinesis:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AllowLogsCreateLogGroup",
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Sid": "AllowLogsCreateLogStreamPutEvents",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
EOF
}

// Renders the lambda function payload for deployment zip file
data "archive_file" "lambda_zip" {
    type        = "zip"
    source_dir  = "code_lambda"
    output_path = "deploys/lambda-update-route53-${var.project_name_short}-${var.project_version}.zip"
}

// Upload function deployment file to S3 bucket
resource "aws_s3_bucket_object" "lambda_zip_to_s3" {
  depends_on       = ["data.archive_file.lambda_zip"] # wait for deployment zip to be created
  bucket = "${aws_s3_bucket.state_bucket.id}"
  key    = "${var.project_name_short}/lambda-update-route53-${var.project_name_short}-${var.project_version}.zip"
  source = "deploys/lambda-update-route53-${var.project_name_short}-${var.project_version}.zip"
}

// Lambda function, use deployment file, uploaded to S3 bucket
resource "aws_lambda_function" "lambda_function_from_s3" {
  function_name    = "lambda-update-route53-${var.project_name_short}-function"
  description      = "lambda-update-route53 ${var.project_name} lambda function"
  role             = "${aws_iam_role.iam_role_for_lambda.arn}"
  handler          = "lambda_execute.lambda_handler"
  runtime          = "python2.7"

  s3_bucket        = "${aws_s3_bucket.state_bucket.id}"
  s3_key           = "${aws_s3_bucket_object.lambda_zip_to_s3.id}"

  timeout = 120

  # environment {
  #   variables = {
  #     # Pass env variables to function
  #     foo = "bar"
  #   }
  # }
}

// Outputs
output "__post_deploy_config_1st" {
  value = "interact with lambda using: python code_local/update_route53.py --aws_domain ${var.project_vars["domain"]} --aws_stream_name ${aws_kinesis_stream.stream_to_lambda.name} --aws_partition_key ${var.project_vars["partition_key"]}"
}