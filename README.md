# kinesis_consumer

This script is used to consume data from AWS Kinesis Stream and print out in the console.

## How to use
`python kinesis_consumer.py -s streamName -p profile -r region`

## Inputs

| Name | Description | Option | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| stream_name | A name to identify the kinesis stream | `-s` or `--stream=` | - | yes |
| profile | credentials to access the kinesis stream | `-p` or `--profile=` | - | yes |
| region | AWS region where the kinesis stream exists | `-r` or `--region=` | - | yes |
| shard_iterator_type | Determines how the shard iterator is used to start reading data records from the shard | `-t` or `--shard-iterator-type=` | `LATEST` | no |
## Outputs

print out records from the kinesis stream in console.
