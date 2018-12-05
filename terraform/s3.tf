// State bucket, available for storing data
resource "aws_s3_bucket" "state_bucket" {
  bucket = "lambda-update-route53-${var.project_name_short}-state"
  acl    = "private"

  force_destroy = true

  versioning {
    enabled = true
  }

  tags = "${merge(
    local.aws_tags,
    map(
      "Name", "lambda-update-route53-${var.project_name_short}-state"
    )
  )}"
}
