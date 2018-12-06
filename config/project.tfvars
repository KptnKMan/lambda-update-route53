// Deploy variables file
// Variables here override the default variables file
// Variables here are overriden by command line and ENV variables at runtime

// Configure where to store config files, like state
# project_config_location = "config"

// Set AWS credentials and region
// Put these in here if you are not using ENV VARs
# aws_access_key          = "reYOURACCESSKEYHEREg"
# aws_secret_key          = "rePUTYOURSUPERSECRETHERETHISISANEXAMPLEr"
# aws_region              = "eu-west-1"

// Name of project, used for tagging
project_name            = "Kareem POC"

// Short name of project, used for naming and tagging
project_name_short      = "kareempoc"

// Version to be used for deploying Lambda function
project_version         = "0.1"

// List of project variables to use in project, set as ENV VARs in lambda
project_vars = {
    ip                  = "1.2.3.4" # ip to set, used for testing
    domain              = "somedomain.com" # domain to update, used for testing
    stream_name         = "lambda-update-route53" # name of kinesis stream, for testing
    partition_key       = "shardId-000000000000" # partition key of kinesis stream
    uuid                = "1234-5678-0123" # uuid to set, used for testing
    shard_count         = "1" # shard count of kinesis stream
    retention_period    = "48" # how long to keep messages (hrs) in kinesis stream
    batch_size          = "1" # how many messages to collect at a time from kinesis stream
    stream_start        = "TRIM_HORIZON" # TRIM_HORIZON or LATEST
}

// Common Tags for all resources in deployment
project_tags = {
  Role                  = "Dev"
  Service               = "Base Infrastructure"
  Business-Unit         = "INFRE"
  Owner                 = "OpsEng"
  Purpose               = "Terraform Lambda Update Route53"
}