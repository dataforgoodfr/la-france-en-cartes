# The state of this module lives in the bucket it creates.
# Bootstrap (bucket not created yet): see README.md.
terraform {
  backend "s3" {
    bucket = var.state_bucket_name
    key    = "backend/terraform.tfstate"

    region = "eu-west-1"

    endpoints = {
      s3 = "https://cellar-c2.services.clever-cloud.com"
    }

    skip_credentials_validation = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
  }
}
