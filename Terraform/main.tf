terraform {
  backend "s3" {
    bucket         = "devops-directive-tf-state-uchiha"
    key            = "03-basics/import-bootstrap/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locking"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket        = "devops-directive-tf-state-uchiha" 
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "terraform_bucket_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_crypto_conf" {
  bucket = aws_s3_bucket.terraform_state.bucket 
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locking"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}

# Create a new VPC
resource "aws_vpc" "my_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

# Create an internet gateway and attach it to the VPC
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id
}

# Create a public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24" 
  availability_zone       = "us-east-1a"  
  map_public_ip_on_launch = true
}

# Create private subnets
resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.2.0/24" 
  availability_zone = "us-east-1a"  
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.3.0/24" 
  availability_zone = "us-east-1b"  
}

# Create a NAT Gateway and Elastic IP
resource "aws_eip" "nat_eip" {}

resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet.id
}

# Create a route table for the private subnets
resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.my_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gateway.id
  }
}

# Associate private subnets with the route table
resource "aws_route_table_association" "private_subnet_1_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_route_table.id
}

resource "aws_route_table_association" "private_subnet_2_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_route_table.id
}

# Create a security group for instances
resource "aws_security_group" "instance_sg" {
  name   = "instance-security-group"
  vpc_id = aws_vpc.my_vpc.id

  # Allow inbound traffic on port 80 from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound traffic to anywhere
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an ALB security group
resource "aws_security_group" "alb_security_group" {
  name   = "alb-security-group"
  vpc_id = aws_vpc.my_vpc.id

  # Allow inbound traffic on port 80 from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound traffic to anywhere
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Allow inbound traffic on port 80 for the instances
resource "aws_security_group_rule" "allow_http_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.instance_sg.id
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

variable "mongo_url" {}

# Launch instances
resource "aws_instance" "instance_1" {
  ami             = "ami-011899242bb902164" # Ubuntu 20.04 LTS // us-east-1
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.instance_sg.id]  
  user_data       = <<-EOF
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo docker pull xahmedmahmoudx/my-frontend:latest
    sudo docker run -d -p 80:80 xahmedmahmoudx/my-frontend:latest
    sudo docker pull xahmedmahmoudx/backend:latest
    export MONGO_URL="${var.mongo_url}"  
    sudo docker run -d -p 3000:6000 -e MONGO_URL xahmedmahmoudx/backend:latest
  EOF
  tags = {
    Name = "Instance-1"
  }
}

resource "aws_instance" "instance_2" {
  ami             = "ami-011899242bb902164" # Ubuntu 20.04 LTS // us-east-1
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.instance_sg.id] 
  user_data       = <<-EOF
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo docker pull xahmedmahmoudx/my-frontend:latest
    sudo docker run -d -p 80:80 xahmedmahmoudx/my-frontend:latest
    sudo docker pull xahmedmahmoudx/backend:latest
    export MONGO_URL="${var.mongo_url}" 
    sudo docker run -d -p 3000:6000 -e MONGO_URL xahmedmahmoudx/backend:latest
  EOF
  tags = {
    Name = "Instance-2"
  }
}
