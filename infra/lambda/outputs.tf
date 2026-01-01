output "lambda_info" {
  value = {
    for k, v in aws_lambda_function.this : k => {
      arn           = v.arn
      function_name = v.function_name
      invoke_arn    = v.invoke_arn
    }
  }
}
