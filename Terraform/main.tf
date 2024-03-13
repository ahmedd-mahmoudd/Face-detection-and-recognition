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
resource "aws_subnet" "frontend_subnet_1" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.1.0/24" 
  availability_zone = "us-east-1a"  
}

resource "aws_subnet" "frontend_subnet_2" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.2.0/24" 
  availability_zone = "us-east-1b"  
}

# Create private subnets
resource "aws_subnet" "backend_subnet_1" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.3.0/24" 
  availability_zone = "us-east-1a"  
}

resource "aws_subnet" "backend_subnet_2" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.4.0/24" 
  availability_zone = "us-east-1b"  
}

# Create a 2 NAT Gateway and Elastic IP
resource "aws_eip" "nat_eip_1" {}

resource "aws_eip" "nat_eip_2" {}

resource "aws_nat_gateway" "nat_gateway_1" {
  allocation_id = aws_eip.nat_eip_1.id
  subnet_id     = aws_subnet.backend_subnet_1.id
  depends_on    = [aws_eip.nat_eip_1]
}

resource "aws_nat_gateway" "nat_gateway_2" {
  allocation_id = aws_eip.nat_eip_2.id
  subnet_id     = aws_subnet.backend_subnet_2.id
  depends_on    = [aws_eip.nat_eip_2]
}

# Create a route table for the backend subnets
resource "aws_route_table" "backend_subnet_1_route_table" {
  vpc_id = aws_vpc.my_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gateway_1.id
  }
}

resource "aws_route_table" "backend_subnet_2_route_table" {
  vpc_id = aws_vpc.my_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat_gateway_2.id
  }
}

# Associate private subnets with the route table
resource "aws_route_table_association" "backend_subnet_1_association" {
  subnet_id      = aws_subnet.backend_subnet_1.id
  route_table_id = aws_route_table.backend_subnet_1_route_table.id
}

resource "aws_route_table_association" "backend_subnet_2_association" {
  subnet_id      = aws_subnet.backend_subnet_2.id
  route_table_id = aws_route_table.backend_subnet_2_route_table.id
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

# Create a security group for instances
resource "aws_security_group" "instance_frontend_sg" {
  name   = "frontend-security-group"
  vpc_id = aws_vpc.my_vpc.id

  # Allow inbound traffic on port 80 from ALB
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_security_group.id]
  }

  # Allow outbound traffic to anywhere
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "instance_backend_sg" {
  name   = "backend-security-group"
  vpc_id = aws_vpc.my_vpc.id

  # Allow inbound traffic on port 3000 from ALB
  ingress {
    from_port       = 3000
    to_port         = 3000
    protocol        = "tcp"
    security_groups = [aws_security_group.instance_frontend_sg.id]
  }

  # Allow outbound traffic to anywhere
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an ALB
resource "aws_lb" "my_alb" {
  name               = "my-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_security_group.id]
  subnets            = [aws_subnet.frontend_subnet_1.id, aws_subnet.frontend_subnet_2.id]

  tags = {
    Name = "My ALB"
  }
}

# Create a target group
resource "aws_lb_target_group" "my_target_group" {
  name     = "my-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.my_vpc.id

  health_check {
    path = "/"
  }
}

# Create a listener for the ALB
resource "aws_lb_listener" "my_listener" {
  load_balancer_arn = aws_lb.my_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_target_group.arn
  }
}

# Launch instances
resource "aws_instance" "instance_frontend_sg" {
  ami           = "ami-011899242bb902164" # Ubuntu 20.04 LTS // us-east-1
  instance_type = "t2.micro"
  security_groups = [aws_security_group.instance_frontend_sg.id]  
  user_data     = <<-EOF
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo docker pull xahmedmahmoudx/my-frontend:latest
    sudo docker run -d -p 80:80 xahmedmahmoudx/my-frontend:latest
  EOF
  tags = {
    Name = "Instance-front-end"
  }
}

resource "aws_instance" "backend_instance_sg" {
  ami           = "ami-011899242bb902164" # Ubuntu 20.04 LTS // us-east-1
  instance_type = "t2.micro"
  security_groups = [aws_security_group.instance_backend_sg.id] 
  user_data     = <<-EOF
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo docker pull xahmedmahmoudx/backend:latest
    export MONGO_URL="${var.mongo_url}" 
    sudo docker run -d -p 3000:6000 -e MONGO_URL xahmedmahmoudx/backend:latest
  EOF
  tags = {
    Name = "Instance-back-end"
  }
}
