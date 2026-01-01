resource "aws_dynamodb_table" "this" {
  name         = "agent-gallery"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "agent_id"

  attribute {
    name = "agent_id"
    type = "S"
  }

  tags = {
    Project = "agent-gallery"
  }
}

output "table_arn" {
  value = aws_dynamodb_table.this.arn
}

output "table_name" {
  value = aws_dynamodb_table.this.name
}
