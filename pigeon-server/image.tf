resource "docker_image" "server" {
  name = "${aws_ecr_repository.server.repository_url}:latest"
  build {
    context = "."
  }
}
resource "docker_registry_image" "server" {
  name = docker_image.server.name
}