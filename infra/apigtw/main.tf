resource "aws_api_gateway_rest_api" "this" {
  name        = "agent-gallery"
  description = "API para galeria de agentes"
}

locals {
  routes = {
    "agent"   = { method = "POST", lambda_key = "create" }
    "gallery" = { method = "GET", lambda_key = "get" }
    "predict" = { method = "POST", lambda_key = "predict" }
  }
}

resource "aws_api_gateway_resource" "res" {
  for_each    = local.routes
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = each.key
}

resource "aws_api_gateway_method" "meth" {
  for_each      = local.routes
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.res[each.key].id
  http_method   = each.value.method
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "int" {
  for_each                = local.routes
  rest_api_id             = aws_api_gateway_rest_api.this.id
  resource_id             = aws_api_gateway_resource.res[each.key].id
  http_method             = aws_api_gateway_method.meth[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_info[each.value.lambda_key].invoke_arn

  timeout_milliseconds = 40000
}

resource "aws_lambda_permission" "apigw_lambda" {
  for_each      = local.routes
  statement_id  = "AllowExecutionFromAPIGateway-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_info[each.value.lambda_key].function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.this.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "this" {
  depends_on  = [aws_api_gateway_integration.int]
  rest_api_id = aws_api_gateway_rest_api.this.id
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.this.id
  rest_api_id   = aws_api_gateway_rest_api.this.id
  stage_name    = "prod"
}

output "base_url" {
  value = aws_api_gateway_stage.prod.invoke_url
}
