// Kinesis Stream to publish to Lambda
resource "aws_kinesis_stream" "stream_to_lambda" {
  name             = "lambda-update-route53-${var.project_name_short}-stream"
  shard_count      = "${var.project_vars["shard_count"]}"
  retention_period = "${var.project_vars["retention_period"]}"

#   shard_level_metrics = [
#     "IncomingBytes",
#     "OutgoingBytes",
#   ]

 tags = "${merge(
   local.aws_tags,
   map(
     "Name", "lambda-update-route53-${var.project_name_short}-stream"
   )
 )}"
}

// Link up Lambda function
resource "aws_lambda_event_source_mapping" "publish_to_lambda_from_s3" {
  batch_size        = "${var.project_vars["batch_size"]}"
  event_source_arn  = "${aws_kinesis_stream.stream_to_lambda.arn}"
  enabled           = true
  function_name     = "${aws_lambda_function.lambda_function_from_s3.arn}"
  starting_position = "${var.project_vars["stream_start"]}"
}