variable "project_id" {
  type        = string
  description = "The GCP project ID to deploy into."
}

variable "region" {
  type        = string
  description = "The preferred GCP availability zone."
  default     = "us-central1"
}

variable "secret_flashback_webhook" {
  type        = string
  description = "The webhook for the flashback notifications."
}
