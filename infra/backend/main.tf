resource "clevercloud_cellar" "backend" {
  name = var.cellar_name

  lifecycle {
    prevent_destroy = true
  }
}

resource "clevercloud_cellar_bucket" "backend_bucket" {
  cellar_id = clevercloud_cellar.backend.id
  id        = var.state_bucket_name

  lifecycle {
    prevent_destroy = true
  }
}
