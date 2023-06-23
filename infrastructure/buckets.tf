resource "google_storage_bucket" "datalake" {
  name = "flashback-application-datalake"
  location = "US"
}

resource "google_storage_bucket" "artifacts" {
  name = "flashback-application-artifacts"
  location = "US"
}
