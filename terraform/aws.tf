// Declare AWS provider for basically everything to follow
provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  # profile    = "customprofile"
  region = "${var.aws_region}"
}

// Define the common tags for all resources
// https://github.com/hashicorp/terraform/blob/master/website/docs/configuration/locals.html.md
locals {
  aws_tags = {
    Role           = "${var.project_tags["Role"]}"
    Service        = "${var.project_tags["Service"]}"
    Business-Unit  = "${var.project_tags["Business-Unit"]}"
    Owner          = "${var.project_tags["Owner"]}"
    Purpose        = "${var.project_tags["Purpose"]}"
    Terraform      = "True"
  }
}
# Extra Tags:
# Name: "Some Resource" <-- required
#
# Use common tags in resources with below example:
#
#  tags = "${merge(
#    local.aws_tags,
#    map(
#      "Name", "awesome-app-server"
#    )
#  )}"
