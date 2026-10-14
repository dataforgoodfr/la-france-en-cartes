variable "clever_organisation" {
  type      = string
  sensitive = true
}

variable "state_passphrase" {
  type        = string
  sensitive   = true
  description = "Passphrase encrypting the state and plans (at least 16 characters)"

  validation {
    condition     = length(var.state_passphrase) >= 16
    error_message = "state_passphrase must be at least 16 characters long."
  }
}

variable "cellar_name" {
  type        = string
  default     = "tfstate"
  description = "Name of the Cellar add-on (changing it replaces the add-on)"
}

variable "state_bucket_name" {
  type        = string
  default     = "tfstate-bucket-d4g-lfe4"
  description = "Name of the Cellar bucket holding the tfstate"
}
