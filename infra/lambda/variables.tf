variable "lambda_names" {
  type    = set(string)
  default = ["create", "get", "predict"]
}
