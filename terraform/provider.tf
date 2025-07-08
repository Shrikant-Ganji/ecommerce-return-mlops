terraform {
  required_providers {
    render = {
      source  = "render/render"
      version = "~> 0.6.0"
    }
  }
}

provider "render" {
  api_key = var.render_api_key
}
