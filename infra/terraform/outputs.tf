output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.main.endpoint
}

output "ec2_public_ip" {
  description = "EC2 app server public IP"
  value       = aws_instance.app.public_ip
}

output "app_url" {
  description = "Application URL (FastAPI backend)"
  value       = "http://${aws_instance.app.public_ip}:8000"
}

output "ui_url" {
  description = "Streamlit UI URL"
  value       = "http://${aws_instance.app.public_ip}:8501"
}

output "ssh_command" {
  description = "SSH command to connect to the app server"
  value       = "ssh ec2-user@${aws_instance.app.public_ip}"
}
