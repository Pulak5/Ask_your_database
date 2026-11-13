# ---------------------------------------------------------------------------
# Data sources
# ---------------------------------------------------------------------------

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# ---------------------------------------------------------------------------
# Security groups
# ---------------------------------------------------------------------------

resource "aws_security_group" "app" {
  name        = "${var.app_name}-app-sg"
  description = "App server security group"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "FastAPI backend"
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Streamlit UI"
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
    description = "SSH admin access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }

  tags = {
    Name        = "${var.app_name}-app-sg"
    Environment = var.environment
  }
}

resource "aws_security_group" "db" {
  name        = "${var.app_name}-db-sg"
  description = "RDS security group — only accessible from app"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
    description     = "PostgreSQL from app server"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }

  tags = {
    Name        = "${var.app_name}-db-sg"
    Environment = var.environment
  }
}

# ---------------------------------------------------------------------------
# RDS PostgreSQL
# ---------------------------------------------------------------------------

resource "random_id" "db_suffix" {
  byte_length = 4
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.app_name}-db-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name        = "${var.app_name}-db-subnet-group"
    Environment = var.environment
  }
}

resource "aws_db_instance" "main" {
  identifier        = "${var.app_name}-db-${random_id.db_suffix.hex}"
  engine            = "postgres"
  engine_version    = "16.3"
  instance_class    = var.db_instance_class
  allocated_storage = 20
  db_name           = "ask_your_db"
  username          = "app"
  password          = var.db_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  publicly_accessible    = false
  skip_final_snapshot    = true

  backup_retention_period = 7
  deletion_protection     = false

  tags = {
    Name        = "${var.app_name}-db"
    Environment = var.environment
  }
}

# ---------------------------------------------------------------------------
# IAM — EC2 role with Bedrock access
# ---------------------------------------------------------------------------

resource "aws_iam_role" "app" {
  name = "${var.app_name}-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })

  tags = {
    Name        = "${var.app_name}-app-role"
    Environment = var.environment
  }
}

resource "aws_iam_role_policy" "bedrock" {
  name = "bedrock-invoke"
  role = aws_iam_role.app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["bedrock:InvokeModel"]
      Resource = "*"
    }]
  })
}

resource "aws_iam_instance_profile" "app" {
  name = "${var.app_name}-profile"
  role = aws_iam_role.app.name
}

# ---------------------------------------------------------------------------
# EC2 Application Server
# ---------------------------------------------------------------------------

resource "aws_instance" "app" {
  ami                  = data.aws_ami.al2023.id
  instance_type        = var.instance_type
  vpc_security_group_ids = [aws_security_group.app.id]
  iam_instance_profile = aws_iam_instance_profile.app.name

  user_data = base64encode(templatefile("${path.module}/userdata.sh.tpl", {
    db_endpoint = aws_db_instance.main.endpoint
    db_password = var.db_password
    aws_region  = var.aws_region
  }))

  tags = {
    Name        = "${var.app_name}-app"
    Environment = var.environment
  }
}
