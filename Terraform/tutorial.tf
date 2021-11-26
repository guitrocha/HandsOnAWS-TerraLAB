
provider "aws"{
    region = "us-east-1"
}

resource "aws_mq_broker" "fila-pokemon" {
    broker_name = "fila-pokemon"
    engine_type = "ActiveMQ"
    engine_version = "5.16.2"
    host_instance_type = "mq.t3.micro"
    publicly_accessible = true

    user {
        username = local.credentials.username
        password = local.credentials.password
        console_access = true
    }
}

data "aws_secretsmanager_secret_version" "mq_user" {
    secret_id = "tutorial/mq/users"
}

locals {
    credentials = jsondecode(
        data.aws_secretsmanager_secret_version.mq_user.secret_string
    )
}

data "aws_vpc" "default" {
    default = true
}

data "aws_security_group" "default" {
    name = "default"
    vpc_id = data.aws_vpc.default.id
}

resource "aws_security_group_rule" "ingress_rules_web" {
  security_group_id = data.aws_security_group.default.id
  type              = "ingress"

  cidr_blocks      = ["0.0.0.0/0"]
  description      = "web console"

  from_port = 8162
  to_port   = 8162
  protocol  = "tcp"
}

resource "aws_security_group_rule" "ingress_rules_stomp" {
  security_group_id = data.aws_security_group.default.id
  type              = "ingress"

  cidr_blocks      = ["0.0.0.0/0"]
  description      = "stomp"

  from_port = 61614
  to_port   = 61614
  protocol  = "tcp"
}

resource "aws_security_group_rule" "ingress_rules_openwire" {
  security_group_id = data.aws_security_group.default.id
  type              = "ingress"

  cidr_blocks      = ["0.0.0.0/0"]
  description      = "open wire"

  from_port = 61617
  to_port   = 61617
  protocol  = "tcp"
}