resource "google_cloud_scheduler_job" "flashback" {
  name        = "flashback"
  schedule    = "0 0 * * *"
  region      = var.region
  description = "Starts a job to send a flashback notification."

  pubsub_target {
    topic_name = google_pubsub_topic.flashback.id
    data = base64encode(jsonencode({ "date": formatdate("YYYYMMDD", timestamp()) }))
  }
}
