terraform {
  required_version = ">= 1.8"

  required_providers {
    clevercloud = {
      source  = "clevercloud/clevercloud"
      version = "2.0.0"
    }
  }
}
