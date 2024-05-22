resource "aws_lb_target_group" "server" {
    name = "server"
    port = 6400
    protocol = "HTTP"
    vpc_id = aws_security_group.server.vpc_id
    target_type = "ip"

    health_check {
        path = "/api/v1/health"
        port = "6400"
        protocol = "HTTP"
        healthy_threshold = 2
        unhealthy_threshold = 2
        timeout = 5
        interval = 10
    }
}

resource "aws_lb" "server" {
    name = "server"
        internal = false
        load_balancer_type = "application"
        subnets = data.aws_subnets.private.ids
        security_groups = [aws_security_group.server-lb.id]
}

resource "aws_security_group" "server-lb" {
    name = "server-lb"
    description = "server Security Group"

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_lb_listener" "server" {
    load_balancer_arn = aws_lb.server.arn
    port = "80"
    protocol = "HTTP"

    default_action {
        type = "forward"
        target_group_arn = aws_lb_target_group.server.arn
    }
}