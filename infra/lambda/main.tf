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
