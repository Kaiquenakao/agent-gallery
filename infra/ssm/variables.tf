variable "table_name" {
  description = "O nome da tabela que será guardado no SSM"
  type        = string
  default     = "agent-gallery"
}

variable "openai_api_key" {
  description = "Chave da API OpenAI para ser guardada no SSM"
  type        = string
}
