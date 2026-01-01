module "lambdas" {
  source = "./infra/lambda"
}

module "api_gateway" {
  source      = "./infra/apigtw"
  lambda_info = module.lambdas.lambda_info
}

output "api_url" {
  value = module.api_gateway.base_url
}
