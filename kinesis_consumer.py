import time
import boto3
import getopt
import sys

stream_name = None
profile = None
region = None
shard_iterator_type = 'LATEST'

help_info = """
[*] Help info:
-s, --stream:
    A name to identify the kinesis stream.

-p, --profile:
    Credentials to access the kinesis stream.
    
-r, --region:
    AWS region where the kinesis stream exists.
    
-t, --shard-iterator-type:
    Determine how shard iterator is used to start reading data records from the shard. Valid values are AT_SEQUENCE_NUMBER, AFTER_SEQUENCE_NUMBER, TRIM_HORIZON, LATEST. Default is LATEST.
""".strip()

opts, args = getopt.getopt(sys.argv[1:], '-h-s:-p:-r:-t:',
                           ['help', 'stream=', 'profile=', 'region=', 'shard-iterator-type='])
for opt_name, opt_value in opts:
    if opt_name in ('-h', '--help'):
        print(help_info)
        exit()
    elif opt_name in ('-s', '--stream'):
        stream_name = opt_value
    elif opt_name in ('-p', '--profile'):
        profile = opt_value
    elif opt_name in ('-r', '--region'):
        region = opt_value
    elif opt_name in ('-t', '--shard-iterator-type'):
        shard_iterator_type = opt_value

if any([stream_name is None, profile is None, region is None]):
    print('Please provide all the required parameters')
    exit()

session = boto3.Session(profile_name=profile)
kinesis_client = session.client('kinesis', region_name=region)

response = kinesis_client.describe_stream(StreamName=stream_name)

shard_id = response['StreamDescription']['Shards'][0]['ShardId']

shard_iterator = kinesis_client.get_shard_iterator(StreamName=stream_name,
                                                   ShardId=shard_id,
                                                   ShardIteratorType=shard_iterator_type)

my_shard_iterator = shard_iterator['ShardIterator']

record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator, Limit=2)

while 'NextShardIterator' in record_response:
    record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'], Limit=2)

    print(record_response)

    # wait for 1 second
    time.sleep(1)
