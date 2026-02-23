# ================================
# Terraform Configuration
# ================================

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.50, != 6.14.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.6"
    }
    tls = {
      source  = "hashicorp/tls"
      version = ">= 4.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }

  backend "s3" {}
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Data sources for provider configuration
data "aws_caller_identity" "current" {}

data "aws_ecr_authorization_token" "token" {}

provider "docker" {
  registry_auth {
    address  = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com"
    username = "AWS"
    password = data.aws_ecr_authorization_token.token.password
  }
}

# ================================
# Variables
# ================================

variable "project_name" {
  type        = string
  default     = "manageros"
  description = "Name of the project"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Environment name (production only - set via CI/CD)"
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region"
}

# ECS container image settings
variable "ecr_repository" {
  type        = string
  default     = "manageros-lambda-api"
  description = "ECR repo name for the API image"
}

variable "image_tag" {
  type        = string
  default     = "latest"
  description = "Container image tag to deploy (can be full image URI or just tag)"
}

# Networking
variable "vpc_cidr" {
  type        = string
  default     = "10.20.0.0/16"
  description = "CIDR block for VPC"
}

variable "private_subnet_cidrs" {
  type        = list(string)
  default     = ["10.20.1.0/24", "10.20.2.0/24"]
  description = "CIDR blocks for private subnets"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  default     = ["10.20.100.0/24", "10.20.101.0/24"]
  description = "CIDR blocks for public subnets (ALB)"
}

# Database (Aurora Serverless v2)
variable "db_name" {
  type        = string
  default     = "manageros"
  description = "Database name"
}

variable "db_username" {
  type        = string
  default     = "postgres"
  description = "Database master username"
}

variable "db_password" {
  type        = string
  default     = "postgres"
  description = "Database master password"
}

variable "db_min_acu" {
  type        = number
  default     = 0
  description = "Minimum Aurora Capacity Units (0 enables auto-pause/scale-to-zero)"
}

variable "db_max_acu" {
  type        = number
  default     = 4.0
  description = "Maximum Aurora Capacity Units"
}

variable "db_auto_pause_seconds" {
  type        = number
  default     = 300
  description = "Seconds of inactivity before Aurora pauses (300-86400). Default: 5 minutes"
}

# Infrastructure control
variable "infrastructure_enabled" {
  type        = bool
  default     = false # Set to true to re-enable infrastructure
  description = "Enable/disable ALL infrastructure. Set to false to destroy everything via CI/CD."
}

# Service control (only relevant when infrastructure_enabled = true)
variable "service_enabled" {
  type        = bool
  default     = true
  description = "Enable/disable the service (API + worker) while keeping infrastructure. Set to false to spin down compute only."
}

# ECS runtime configuration
variable "ecs_cpu" {
  type        = number
  default     = 256
  description = "CPU units for ECS task (256 = 0.25 vCPU)"
}

variable "ecs_memory" {
  type        = number
  default     = 512
  description = "Memory for ECS task in MB"
}

variable "ecs_desired_count" {
  type        = number
  default     = 1
  description = "Desired number of ECS tasks (ignored if service_enabled = false)"
}

variable "ecs_min_capacity" {
  type        = number
  default     = 1
  description = "Minimum number of ECS tasks for auto-scaling"
}

variable "ecs_max_capacity" {
  type        = number
  default     = 4
  description = "Maximum number of ECS tasks for auto-scaling"
}

# Worker configuration
variable "worker_cpu" {
  type        = number
  default     = 256
  description = "CPU units for worker task (256 = 0.25 vCPU)"
}

variable "worker_memory" {
  type        = number
  default     = 512
  description = "Memory for worker task in MB"
}

variable "worker_desired_count" {
  type        = number
  default     = 1
  description = "Desired number of worker tasks (ignored if service_enabled = false)"
}

# Env/Secrets for the app
variable "extra_env" {
  description = "Map of extra env vars for the container"
  type        = map(string)
  default = {
    DEBUG = "false"
  }
}

# S3 bucket configuration
variable "s3_bucket_prefix" {
  type        = string
  default     = "manageros-storage"
  description = "S3 bucket name prefix (random suffix will be added)"
}

# ================================
# Infrastructure Module
# ================================

module "infrastructure" {
  count  = var.infrastructure_enabled ? 1 : 0
  source = "./modules/infrastructure"

  # Pass all variables to module
  project_name          = var.project_name
  environment           = var.environment
  aws_region            = var.aws_region
  ecr_repository        = var.ecr_repository
  image_tag             = var.image_tag
  vpc_cidr              = var.vpc_cidr
  private_subnet_cidrs  = var.private_subnet_cidrs
  public_subnet_cidrs   = var.public_subnet_cidrs
  db_name               = var.db_name
  db_username           = var.db_username
  db_password           = var.db_password
  db_min_acu            = var.db_min_acu
  db_max_acu            = var.db_max_acu
  db_auto_pause_seconds = var.db_auto_pause_seconds
  service_enabled       = var.service_enabled
  ecs_cpu               = var.ecs_cpu
  ecs_memory            = var.ecs_memory
  ecs_desired_count     = var.ecs_desired_count
  ecs_min_capacity      = var.ecs_min_capacity
  ecs_max_capacity      = var.ecs_max_capacity
  worker_cpu            = var.worker_cpu
  worker_memory         = var.worker_memory
  worker_desired_count  = var.worker_desired_count
  extra_env             = var.extra_env
  s3_bucket_prefix      = var.s3_bucket_prefix
}

# ================================
# Outputs
# ================================

output "alb_dns_name" {
  description = "The DNS name of the Application Load Balancer"
  value       = var.infrastructure_enabled ? module.infrastructure[0].alb_dns_name : null
}

output "alb_url" {
  description = "The public URL of the Application Load Balancer"
  value       = "https://api.tryarive.com"
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = var.infrastructure_enabled ? module.infrastructure[0].ecs_cluster_name : null
}

output "ecs_service_name" {
  description = "The name of the ECS service"
  value       = var.infrastructure_enabled ? module.infrastructure[0].ecs_service_name : null
}

output "database_endpoint" {
  description = "The Aurora cluster endpoint"
  value       = var.infrastructure_enabled ? module.infrastructure[0].database_endpoint : null
}

output "database_reader_endpoint" {
  description = "The Aurora cluster reader endpoint"
  value       = var.infrastructure_enabled ? module.infrastructure[0].database_reader_endpoint : null
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = var.infrastructure_enabled ? module.infrastructure[0].s3_bucket_name : null
}

output "s3_bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = var.infrastructure_enabled ? module.infrastructure[0].s3_bucket_arn : null
}

output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = var.infrastructure_enabled ? module.infrastructure[0].ecr_repository_url : null
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = var.infrastructure_enabled ? module.infrastructure[0].vpc_id : null
}

output "private_subnet_ids" {
  description = "The IDs of the private subnets"
  value       = var.infrastructure_enabled ? module.infrastructure[0].private_subnet_ids : []
}

output "app_secrets_arn" {
  description = "ARN of the application secrets in Secrets Manager"
  value       = var.infrastructure_enabled ? module.infrastructure[0].app_secrets_arn : null
}

output "ecs_exec_command" {
  description = "Command to connect to ECS task via Session Manager"
  value       = "make ecs-exec"
}

output "worker_service_name" {
  description = "The name of the worker ECS service"
  value       = var.infrastructure_enabled ? module.infrastructure[0].worker_service_name : null
}

# Route53 DNS outputs
output "route53_nameservers" {
  description = "AWS Route53 nameservers - update these at Namecheap"
  value       = var.infrastructure_enabled ? module.infrastructure[0].route53_nameservers : null
}

output "route53_zone_id" {
  description = "Route53 hosted zone ID"
  value       = var.infrastructure_enabled ? module.infrastructure[0].route53_zone_id : null
}

# SES outputs
output "ses_domain_verification_status" {
  description = "SES domain verification status (check after apply)"
  value       = "Check AWS SES Console for verification status"
}

output "ses_dkim_status" {
  description = "SES DKIM status (check after apply)"
  value       = "Check AWS SES Console for DKIM verification status"
}

output "ses_configuration_set" {
  description = "SES configuration set name"
  value       = var.infrastructure_enabled ? module.infrastructure[0].ses_configuration_set : null
}

output "inbound_emails_bucket" {
  description = "S3 bucket for inbound emails"
  value       = var.infrastructure_enabled ? module.infrastructure[0].inbound_emails_bucket : null
}

output "lambda_function_name" {
  description = "Email webhook Lambda function name"
  value       = var.infrastructure_enabled ? module.infrastructure[0].lambda_function_name : null
}
