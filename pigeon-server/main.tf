terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 4.0"
        }
        docker = {
            source = "kreuzwerker/docker"
            version = "3.0.2"
        }
    }
}

provider "aws" {
    region = "us-east-1"
    shared_credentials_files = ["./credentials"]
    default_tags {
        tags = {
            Course       = "CSSE6400"
            Name         = "Pigeon"
            Automation   = "Terraform"
        }
    }
}

data "aws_ecr_authorization_token" "ecr_token" {}

provider "docker" {
    registry_auth {
        address = data.aws_ecr_authorization_token.ecr_token.proxy_endpoint
        username = data.aws_ecr_authorization_token.ecr_token.user_name
        password = data.aws_ecr_authorization_token.ecr_token.password
    }
}

resource "aws_ecr_repository" "server" {
    name = "server"
}

resource "local_file" "url" {
    content = "http://${aws_lb.server.dns_name}/api/v1/"
    filename = "../pigeon-client/client/api.txt"

    depends_on = [ 
        aws_lb.server
     ]
}

locals {
    database_username = "administrator"
    database_password = "verySecretPassword"
}

data "aws_iam_role" "lab" {
  name = "LabRole"
}

data "aws_vpc" "default" {
    default = true
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}