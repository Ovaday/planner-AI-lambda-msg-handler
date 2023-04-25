import sentry_sdk, asyncio
from sentry_sdk import capture_exception, set_user
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import psycopg2

from requestHelpers import *


dynamodb_client = boto3.client('dynamodb')

secrets = get_aws_secrets('DEV_SECRETS_NAME')
TOKEN = secrets['TG_BOT_TOKEN']
application = ApplicationBuilder().token(TOKEN).build()


def set_db_connection():
    DB_USER = secrets['DB_USER']
    DB_PASSWORD = secrets['DB_PASSWORD']
    DB_HOST = secrets['DB_HOST']
    DB_NAME = secrets['DB_NAME']

    connection = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                                  database=DB_NAME)
    return connection


db_connection = set_db_connection()

from commandHandlers import *
from messageHandlers import *
from audioHandlers import audio
from messageHelpers import message_specific

sentry_sdk.init(
    dsn=secrets["SENTRY_LA_MESSAGES"],
    integrations=[
        AwsLambdaIntegration(timeout_warning=True),
    ],
    traces_sample_rate=1.0,
)

format = {"message_specific": {"chat_id": 123, "message": "test"}}
def lambda_handler(event, context):
    print(event['body'])
    body_json = json.loads(event['body'])
    if 'message_specific' in body_json:
        msg_specific = body_json['message_specific']
        if 'chat_id' in msg_specific and 'message' in msg_specific:
            try:
                return asyncio.get_event_loop().run_until_complete(message_specific(msg_specific['chat_id'],
                                                                                    application, msg_specific['message']))
            except Exception as exc:
                set_user({"id": f"{msg_specific['chat_id']}"})
                capture_exception(exc)
                return error_response
    try:
        return asyncio.get_event_loop().run_until_complete(main(event, context))
    except Exception as exc:
        capture_exception(exc)
        return error_response


async def main(event, context):
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    audio_handler = MessageHandler(filters.VOICE, audio)
    application.add_handler(audio_handler)

    try:
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )

        return success_response

    except Exception as exc:
        if event and "message" in event and "from" in event['message'] and "id" in event['message']['from']:
            set_user({"id": f"{event['message']['from']['id']}"})
        capture_exception(exc)
        return error_response
