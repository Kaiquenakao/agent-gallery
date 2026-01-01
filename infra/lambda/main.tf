data "aws_caller_identity" "current" {}

data "archive_file" "lambda_zip" {
  for_each    = var.lambda_names
  type        = "zip"
  source_dir  = "${path.module}/src/${each.value}"
  output_path = "${path.module}/src/build/${each.value}.zip"
}

resource "aws_iam_role" "lambda_exec" {
  name = "agent-gallery-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

data "aws_iam_policy" "lambda_basic_execution" {
  name = "AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_lambda_function" "this" {
  for_each      = var.lambda_names
  function_name = "agent-gallery-${each.key}"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.10"

  filename         = data.archive_file.lambda_zip[each.key].output_path
  source_code_hash = data.archive_file.lambda_zip[each.key].output_base64sha256

  depends_on = [aws_iam_role_policy_attachment.lambda_logs]
}

variable "dynamodb_table_arn" {
  type = string
}

resource "aws_iam_role_policy" "dynamo_access" {
  name = "agent-gallery-dynamo-access"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ],
        Effect   = "Allow",
        Resource = var.dynamodb_table_arn
      }
    ]
  })
}


resource "aws_iam_role_policy" "ssm_access" {
  name = "agent-gallery-ssm-access"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:ssm:sa-east-1:${data.aws_caller_identity.current.account_id}:parameter/agent_gallery/*"
      }
    ]
  })
}
