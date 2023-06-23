data "archive_file" "flashback_source" {
    type        = "zip"
    source_dir  = "../src/flashback/flashback"
    output_path = "/tmp/flashback.zip"
}

resource "google_storage_bucket_object" "flashback_archive" {
  content_type = "application/zip"
  bucket = google_storage_bucket.artifacts.name
  source = data.archive_file.flashback_source.output_path

  name   = "flashback-${data.archive_file.flashback_source.output_md5}.zip"
}

resource "google_cloudfunctions_function" "flashback" {
  name        = "flashback"
  description = "Sends a flashback notification to Discord"
  runtime     = "python39"

  
  source_archive_bucket = google_storage_bucket.artifacts.name
  source_archive_object = google_storage_bucket_object.flashback_archive.name

  timeout               = 540
  available_memory_mb   = 2048
  max_instances         = 1

  entry_point           = "main"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.flashback.id
    failure_policy {
      retry = false
    }
  }

  environment_variables = {
    BUCKET = google_storage_bucket.datalake.name
  }

  secret_environment_variables {
    key     = "WEBHOOK"
    secret  = var.secret_flashback_webhook
    version = "latest"
  }
}
