provider "google" {
  credentials  = "../config/zippy-parity-345616-248fc7c31b15.json"
  project      = "zippy-parity-345616"
  region       = "europe-west1"
  zone         = "europe-west1-b"
}

#app-geo port rules
resource "google_compute_firewall" "app-geo-firewall" {
  name    = "app-geo-rule"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22","8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["app-geo"]
}
#db-geo port rules
resource "google_compute_firewall" "db-geo-ssh-firewall" {
  name    = "db-geo-ssh-rule"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["db-geo-ssh"]
}

resource "google_compute_firewall" "db-geo-db-firewall"{
  name    = "db-geo-db-rule"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["db-geo-db"]
}

#app-geo instance
resource "google_compute_instance" "vm-instance-1" {
  name         = "geo-app-terraform" # name of the server
  machine_type = "e2-small" # machine type refer google machine types
  tags         = ["app-geo"] # selecting the vm instances with tags

  boot_disk { 
    initialize_params {
      image = "ubuntu-1804-bionic-v20220325"
    }
  }

  network_interface {
    network = "default"
    access_config {
   }
  }
  metadata = {
    ssh-keys = "gcpuser"
  }
}
#db-geo instance
resource "google_compute_instance" "vm-instance-2" {
  name         = "geo-db-terraform" # name of the server
  machine_type = "e2-micro" # machine type refer google machine types
  tags         = ["db-geo-ssh","db-geo-db"] # selecting the vm instances with tags

  boot_disk {
    initialize_params {
      image = "centos-7-v20220303"
    }
  }

  network_interface {
    network = "default"
    access_config {
   }
  }
  metadata = {
    ssh-keys = "gcpuser"
  }
}
#IP of gcp instances copied to a file hosts file in local system
resource "local_file" "hosts_file" {
  content  = <<EOT
[app_server]
app_host ansible_host=${google_compute_instance.vm-instance-1.network_interface.0.access_config.0.nat_ip}
[db_server]
db_host ansible_host=${google_compute_instance.vm-instance-2.network_interface.0.access_config.0.nat_ip}

EOT  
  filename = "../config/hosts"
}
#IP of gcp instances copied to a file hosts file in local system
resource "local_file" "hosts_file_ip" {
  content  = <<EOT
#!/bin/bash
server_ip='${google_compute_instance.vm-instance-1.network_interface.0.access_config.0.nat_ip}'
db_server_ip='${google_compute_instance.vm-instance-2.network_interface.0.access_config.0.nat_ip}'
EOT  
  filename = "../config/hosts_geo"
}
