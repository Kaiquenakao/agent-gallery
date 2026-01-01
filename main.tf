module "dynamodb" {
  source = "./infra/dynamodb"
}

module "lambdas" {
  source             = "./infra/lambda"
  dynamodb_table_arn = module.dynamodb.table_arn
}

module "api_gateway" {
  source      = "./infra/apigtw"
  lambda_info = module.lambdas.lambda_info
}

output "api_url" {
  value = module.api_gateway.base_url
}

module "ssm" {
  source     = "./infra/ssm"
  table_name = var.table_name
}
