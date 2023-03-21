provider "google" {
  project = "trpg-bot-375507"
  region  = "us-east1"
  zone    = "us-east1-b"
}

# provider "google-beta" {
#   project = "trpg-bot-375507"
#   region  = "us-east1"
#   zone    = "us-east1-b"
# }

terraform {
  backend "gcs" {
    bucket = "terraform-backend-75863"
  }
}

# resource "google_project_service" "firestore" {
#   provider = google-beta
#   service  = "firestore.googleapis.com"
# }

# resource "google_firestore_database" "database" {
#   provider = google-beta
#   count    = 1

#   name        = "(default)"
#   location_id = "us-east1"
#   type        = "FIRESTORE_NATIVE"

#   depends_on = [google_project_service.firestore]
# }

resource "google_compute_instance" "default" {
  name         = "trpg-bot2"
  machine_type = "e2-micro"
  count        = 0

  boot_disk {
    initialize_params {
      image = "projects/cos-cloud/global/images/family/cos-stable"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata = {
    discord-bot-token = var.DISCORD_BOT_TOKEN
  }

  metadata_startup_script = file("startup.sh")
}
