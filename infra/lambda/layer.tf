resource "null_resource" "install_predict_dependencies" {
  provisioner "local-exec" {
    command     = <<EOT
if (Test-Path build) { Remove-Item build -Recurse -Force }
New-Item -ItemType Directory -Path build\python
pip install -r src/predict/requirements.txt -t build\python
EOT
    working_dir = path.module
    interpreter = ["PowerShell", "-Command"]
  }

  triggers = {
    requirements_hash = sha256(file("${path.module}/src/predict/requirements.txt"))
  }
}

data "archive_file" "predict_layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/build"
  output_path = "${path.module}/src/build/predict_layer.zip"

  depends_on = [null_resource.install_predict_dependencies]
}

resource "aws_lambda_layer_version" "predict" {
  filename            = data.archive_file.predict_layer_zip.output_path
  layer_name          = "agent-gallery-predict-layer"
  compatible_runtimes = ["python3.10"]
  source_code_hash    = data.archive_file.predict_layer_zip.output_base64sha256

  depends_on = [data.archive_file.predict_layer_zip]
}
