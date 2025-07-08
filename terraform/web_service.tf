resource "render_service" "ecommerce_return_api" {
  name        = "ecommerce-return-api"
  service_type = "web"

  repo = "https://github.com/your-username/ecommerce-return-mlops.git"

  branch = "main"

  # For Docker service, you might specify the dockerfile path here
  dockerfile_path = "Dockerfile"

  env = {
    ENVIRONMENT = "production"
  }

  # Instance size options: "starter", "basic", "standard", etc.
  plan = "starter"

  region = "oregon"  # or your preferred Render region

  auto_deploy = true
}
