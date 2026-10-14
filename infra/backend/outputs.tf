output "cellar_creds" {
  sensitive = true
  value = {
    host       = clevercloud_cellar.backend.host
    key_id     = clevercloud_cellar.backend.key_id
    key_secret = clevercloud_cellar.backend.key_secret

  }
}
