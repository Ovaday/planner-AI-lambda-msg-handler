import sentry_sdk, asyncio, boto3
from sentry_sdk import capture_exception, set_user
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from requestHelpers import *

dynamodb_client = boto3.client('dynamodb')

secrets = get_aws_secrets('DEV_SECRETS_NAME')
TOKEN = secrets['TG_BOT_TOKEN']
application = ApplicationBuilder().token(TOKEN).build()

from commandHandlers import *
from messageHandlers import *

sentry_sdk.init(
    dsn=secrets["SENTRY_LA_MESSAGES"],
    integrations=[
        AwsLambdaIntegration(timeout_warning=True),
    ],
    traces_sample_rate=1.0,
)


def lambda_handler(event, context):
    return asyncio.get_event_loop().run_until_complete(main(event, context))


async def main(event, context):
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

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
