provider "aws" {
  access_key = ""
  secret_key = ""
  region     = "us-east-2"
}


# BUCKET
resource "random_string" "id" {
  length = "3"
  special = false
  upper = false
}
resource "aws_s3_bucket" "bucket" {
  bucket = "dataquest-${random_string.id.result}"
  #bucket = "rearcdataquest"
}
resource "aws_s3_bucket_public_access_block" "bucket" {
  bucket = aws_s3_bucket.bucket.id
  block_public_acls   = true
  block_public_policy = true
}
resource "aws_s3_bucket_object" "directory" {
  bucket       = "${aws_s3_bucket.bucket.id}"
  key          = "pr/"
}
#resource "aws_s3_bucket_notification" "bucket_notification" {
#  bucket = aws_s3_bucket.bucket.id
#  depends_on = [aws_sqs_queue.queue]
#  queue {
#	  id 	= aws_sqs_queue.queue.id
#    queue_arn     = aws_sqs_queue.queue.arn
#    events        = ["s3:ObjectCreated:*"]
#  }
#}



# SQS QUEUE
resource "aws_sqs_queue" "queue" {
  name = "s3-event-notification-queue"
  policy  = "${file("iam/sqs_policy.json")}"
}



# TRIGGER
resource "aws_cloudwatch_event_rule" "run_data_fetch" {
  name        = "run_data_fetch"
  description = "Daily trigger"
  schedule_expression  = "rate(24 hours)"
}
resource "aws_cloudwatch_event_target" "timer_run_data_fetch" {
  rule      = aws_cloudwatch_event_rule.run_data_fetch.name
  target_id = "data_fetch"
  arn       = aws_lambda_function.data_fetch.arn
}
resource "aws_lambda_permission" "allow_run_data_fetch" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.data_fetch.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.run_data_fetch.arn}"
}



# LAMBDA
resource "aws_lambda_function" "data_fetch" {
  function_name = "data_fetch"
  role          = "${aws_iam_role.lambda_role.arn}"
  handler       = "code.data_fetch.orchestrator"
  source_code_hash = "${filebase64sha256("outputs/data_fetch.zip")}"
  runtime = "python3.7"
  filename      = "outputs/data_fetch.zip"
  #depends_on = [null_resource.install_python_dependencies]
}




# ARCHIVE
data "archive_file" "create_dist_pkg" {
  source_dir  = "${path.cwd}/code/" 
  output_path = "outputs/data_fetch.zip"
  type        = "zip"
  #depends_on = ["null_resource.install_python_dependencies"]
}
#resource "null_resource" "install_python_dependencies" {
#  provisioner "local-exec" {
#    command = "bash ${path.module}/scripts/create_pkg.sh"
#    environment = {
#      source_code_path = "code"
#      function_name = "data_fetch"
#      path_module = path.module
#      runtime = "python3.7"
#      path_cwd = path.cwd
#    }
#  }
#}