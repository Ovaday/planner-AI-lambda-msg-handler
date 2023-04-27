from main import *

SQS_TYPE_OPENAI = 'openai'
SQS_TYPE_TG = "telegram"
SQS_TYPE_VERCEL = "vercel"

async def queue_message(recipient: str, message: str, msg_type:str, args=None):
    message_attributes = {
        'recipient': {
            'DataType': 'String',
            'StringValue': recipient
        },
        'type': {
            'DataType': 'String',
            'StringValue': msg_type
        }
    }
    if args:
        for arg in args:
            message_attributes[arg] = args[arg]

    return sqs_client.send_message(
                QueueUrl=secrets["SQS_V1_URL"],
                MessageBody=message,
                DelaySeconds=0,
                MessageAttributes=message_attributes
            )