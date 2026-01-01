# Criar o parâmetro no SSM
resource "aws_ssm_parameter" "table_name" {
  name        = "/agent_gallery/table_name"
  description = "Nome da tabela para a Galeria de Agentes"
  type        = "String"
  value       = var.table_name
}

# Output para ver o ARN do parâmetro criado
output "ssm_parameter_arn" {
  value = aws_ssm_parameter.table_name.arn
}
