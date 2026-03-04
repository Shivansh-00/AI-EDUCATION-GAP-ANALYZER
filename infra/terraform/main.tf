terraform {
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = "us-east-1"
}

# Starter placeholder for production IaC modules:
# - EKS cluster
# - RDS PostgreSQL
# - ElastiCache Redis
# - Neo4j managed instance
