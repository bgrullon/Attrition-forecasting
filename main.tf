terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
variable "aws_access_key_id" {
  type = string
}

variable "aws_secret_access_key" {
  type = string
}

provider "aws" {
  region      = "us-east-1"
  access_key  = var.aws_access_key_id
  secret_key  = var.aws_secret_access_key
}

# Create a random password that includes a number
resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
  numeric          = true
  min_numeric      = 2
}

resource "random_string" "unique_suffix" {
  length  = 6
  special = false
}

# Resources

# AWS S3 Bucket
resource "aws_s3_bucket" "redshift_bucket" {
  bucket = "redshift-bucket-project-4"
  tags = {
    Name        = "Redshift Bucket"
    Environment = "Dev"
  }
}

# IAM Role for Redshift
resource "aws_iam_role" "redshift_iam_role" {
  name = "redshift-s3-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for Redshift to Read from S3
resource "aws_iam_policy" "redshift_s3_policy" {
  name        = "redshift-s3-policy"
  description = "IAM policy for Redshift to read from S3"
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "s3:GetObject",
        Resource = "${aws_s3_bucket.redshift_bucket.arn}/*"
      },
      {
        Effect   = "Allow",
        Action   = "s3:ListBucket",
        Resource = aws_s3_bucket.redshift_bucket.arn
      }
    ]
  })
}

# Attach the IAM Policy to the IAM Role
resource "aws_iam_role_policy_attachment" "redshift_s3_attachment" {
  policy_arn = aws_iam_policy.redshift_s3_policy.arn
  role       = aws_iam_role.redshift_iam_role.name
}

# Redshift Cluster
resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier = "tf-redshift-cluster"
  database_name      = "mydb"
  master_username    = "admin"
  master_password    = random_password.password.result
  node_type          = "dc2.large"
  cluster_type       = "single-node"

  skip_final_snapshot = true

  # Associate the IAM Role with the Redshift Cluster
  iam_roles = [aws_iam_role.redshift_iam_role.arn]
}

resource "aws_secretsmanager_secret" "redshift_connection" {
  description = "Redshift connect details"
  name        = "redshift_secret_${random_string.unique_suffix.result}"
}

resource "aws_secretsmanager_secret_version" "redshift_connection" {
  secret_id = aws_secretsmanager_secret.redshift_connection.id
  secret_string = jsonencode({
    username            = aws_redshift_cluster.redshift_cluster.master_username
    password            = aws_redshift_cluster.redshift_cluster.master_password
    engine              = "redshift"
    host                = aws_redshift_cluster.redshift_cluster.endpoint
    port                = "5439"
    dbClusterIdentifier = aws_redshift_cluster.redshift_cluster.cluster_identifier
  })
}
