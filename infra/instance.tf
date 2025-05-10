# Create an EC2 instance
resource "aws_instance" "mlops_instance" {
  ami                    = "ami-084568db4383264d4"  
  instance_type          = "t2.xlarge"  # Adjust instance type as needed
  key_name               = "mlops_keypair"
  vpc_security_group_ids = [aws_security_group.mlops_sg.id]
  root_block_device {
    volume_size           = 30  # Size in GB
    volume_type           = "gp2"  # General Purpose SSD
    delete_on_termination = true
    tags = {
      Name = "mlops-root-volume"
    }
  }
  tags = {
    Name = "mlops-instance"
  }


}

# Create a security group for the instance
resource "aws_security_group" "mlops_sg" {
  name        = "mlops-security-group"
  description = "Allow SSH and other necessary traffic"

  # SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Consider restricting to your IP for better security
  }

  # Outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# # Output the instance's public IP
# output "instance_public_ip" {
#   value = aws_instance.mlops_instance.public_ip
# }