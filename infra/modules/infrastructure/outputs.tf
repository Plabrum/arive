# ================================
# Module Outputs
# ================================

output "alb_dns_name" {
  description = "The DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "alb_url" {
  description = "The public URL of the Application Load Balancer"
  value       = "https://api.tryarive.com"
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "The name of the ECS service"
  value       = aws_ecs_service.main.name
}

output "database_endpoint" {
  description = "The Aurora cluster endpoint"
  value       = aws_rds_cluster.main.endpoint
}

output "database_reader_endpoint" {
  description = "The Aurora cluster reader endpoint"
  value       = aws_rds_cluster.main.reader_endpoint
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.app.bucket
}

output "s3_bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.app.arn
}

output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.app.repository_url
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "The IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "app_secrets_arn" {
  description = "ARN of the application secrets in Secrets Manager"
  value       = aws_secretsmanager_secret.app_secrets_v2.arn
}

output "ecs_exec_command" {
  description = "Command to connect to ECS task via Session Manager"
  value       = "make ecs-exec"
}

output "worker_service_name" {
  description = "The name of the worker ECS service"
  value       = aws_ecs_service.worker.name
}

output "route53_nameservers" {
  description = "AWS Route53 nameservers - update these at Namecheap"
  value       = aws_route53_zone.main.name_servers
}

output "route53_zone_id" {
  description = "Route53 hosted zone ID"
  value       = aws_route53_zone.main.zone_id
}

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
  value       = aws_ses_configuration_set.main.name
}

output "inbound_emails_bucket" {
  description = "S3 bucket for inbound emails"
  value       = aws_s3_bucket.inbound_emails.bucket
}

output "lambda_function_name" {
  description = "Email webhook Lambda function name"
  value       = aws_lambda_function.email_webhook.function_name
}
