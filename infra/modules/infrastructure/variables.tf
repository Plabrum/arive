# ================================
# Module Variables
# ================================

variable "project_name" {
  type        = string
  description = "Name of the project"
}

variable "environment" {
  type        = string
  description = "Environment name (production only - set via CI/CD)"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
}

# ECS container image settings
variable "ecr_repository" {
  type        = string
  description = "ECR repo name for the API image"
}

variable "image_tag" {
  type        = string
  description = "Container image tag to deploy (can be full image URI or just tag)"
}

# Networking
variable "vpc_cidr" {
  type        = string
  description = "CIDR block for VPC"
}

variable "private_subnet_cidrs" {
  type        = list(string)
  description = "CIDR blocks for private subnets"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  description = "CIDR blocks for public subnets (ALB)"
}

# Database (Aurora Serverless v2)
variable "db_name" {
  type        = string
  description = "Database name"
}

variable "db_username" {
  type        = string
  description = "Database master username"
}

variable "db_password" {
  type        = string
  description = "Database master password"
}

variable "db_min_acu" {
  type        = number
  description = "Minimum Aurora Capacity Units (0 enables auto-pause/scale-to-zero)"
}

variable "db_max_acu" {
  type        = number
  description = "Maximum Aurora Capacity Units"
}

variable "db_auto_pause_seconds" {
  type        = number
  description = "Seconds of inactivity before Aurora pauses (300-86400). Default: 5 minutes"
}

# Service control
variable "service_enabled" {
  type        = bool
  description = "Enable/disable the service (API + worker) while keeping infrastructure. Set to false to spin down compute only."
}

# ECS runtime configuration
variable "ecs_cpu" {
  type        = number
  description = "CPU units for ECS task (256 = 0.25 vCPU)"
}

variable "ecs_memory" {
  type        = number
  description = "Memory for ECS task in MB"
}

variable "ecs_desired_count" {
  type        = number
  description = "Desired number of ECS tasks (ignored if service_enabled = false)"
}

variable "ecs_min_capacity" {
  type        = number
  description = "Minimum number of ECS tasks for auto-scaling"
}

variable "ecs_max_capacity" {
  type        = number
  description = "Maximum number of ECS tasks for auto-scaling"
}

# Worker configuration
variable "worker_cpu" {
  type        = number
  description = "CPU units for worker task (256 = 0.25 vCPU)"
}

variable "worker_memory" {
  type        = number
  description = "Memory for worker task in MB"
}

variable "worker_desired_count" {
  type        = number
  description = "Desired number of worker tasks (ignored if service_enabled = false)"
}

# Env/Secrets for the app
variable "extra_env" {
  description = "Map of extra env vars for the container"
  type        = map(string)
}

# S3 bucket configuration
variable "s3_bucket_prefix" {
  type        = string
  description = "S3 bucket name prefix (random suffix will be added)"
}
