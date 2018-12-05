// Default variables file
// Variables here are used if no variable is set elsewhere
// Variables here are overriden by the deploy variables file

variable project_config_location {
  type                    = "string"
  default                 = "config"
}

variable "aws_access_key" {
  type                    = "string"
}

variable "aws_secret_key" {
  type                    = "string"
}

variable "aws_region" {
  type                    = "string"
  default                 = "eu-west-1"
}

variable "project_name" {
  type                    = "string"
  default                 = "Kareem POC"
}

variable "project_name_short" {
  type                    = "string"
  default                 = "kareempoc"
}

variable "project_version" {
  type                    = "string"
  default                 = "0.1"
}

variable "project_vars" {
  type = "map"
  default = {
    domain                = "mydomain.com"
    ip                    = "1.2.3.4"
    uuid                  = "1234-5678-0123"
    stream_name           = "lambda-update-route53"
    shard_count           = "1"
    retention_period      = "24"
    batch_size            = "1"
    partition_key         = "shardId-000000000000"
    stream_start          = "TRIM_HORIZON"
  }
}

variable "project_tags" {
  type = "map"
  default = {
    Role                  = "Dev"
    Service               = "Base Infrastructure"
    Business-Unit         = "INFRE"
    Owner                 = "OpsEng"
    Purpose               = "Terraform Lambda Route53"
  }
}
