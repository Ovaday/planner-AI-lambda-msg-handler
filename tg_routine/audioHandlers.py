import openai

from main import *
from commandHandlers import start
from serviceHelpers import check_is_chat_approved

import io
import json
import soundfile as sf


async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message, chat_id, chat = await resolve_main_params(db_connection, update)

    if not chat:
        print('no chat')
        return await start(update, context)
    if not await check_is_chat_approved(chat, context, message):
        return

    else:
        mem_file, duration = await process_voice_message(update, context)
        print('processed_voice_message')
        recognized_text = await voice_to_text(chat, mem_file, duration)
        print('recognized_text')
        #await async_assign_last_conversation(chat_id, recognized_text)
        await context.bot.send_message(reply_to_message_id=message.message_id, chat_id=chat_id,
                                       text=f"""{get_label('recognized', chat.language)}: {recognized_text}

        {get_label('processing_wait', chat.language)}""")

        #json_update = json.loads(update.to_json())
        #json_update = audio_json_to_text(json_update, recognized_text)
        #print('audio_json_to_text')
        #new_update = Update.de_json(json_update, context)
        #await chat_gpt_message(new_update, context)


async def process_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_message = await context.bot.get_file(update.message.voice.file_id)
    #voice_file = io.BytesIO()
    #await voice_message.download_to_memory(voice_file)
    local_path = "/tmp/voice_message.ogg"
    voice_message.download(local_path)
    s3_client = boto3.client("s3")

    s3_bucket = os.environ["VOICE_MESSAGES_BUCKET"]
    s3_prefix = f'voice_{update.message.chat_id}_{update.message.message_id}.ogg'
    remote_s3_path = os.path.join("s3://", s3_bucket, s3_prefix)
    print(remote_s3_path)
    s3_client.upload_file(local_path, s3_bucket, s3_prefix)

    #voice_file.seek(0)
    #voice_file.name = f'voice_{update.message.chat_id}_{update.message.message_id}.ogg'

    data, samplerate = sf.read(local_path)
    mem_file = io.BytesIO()
    sf.write(mem_file, data, samplerate, 'PCM_16', format='wav')
    mem_file.seek(0)
    duration = sf.info(mem_file).duration
    mem_file.seek(0)
    mem_file.name = f'voice_{update.message.chat_id}_{update.message.message_id}.wav'
    return mem_file, duration


async def voice_to_text(tg_chat, voice_file, duration):
    openai.api_key = secrets['OPENAI_API']
    model = "whisper-1" # there is no other model
    response = openai.Audio.transcribe(model, voice_file)
    #ToDo: await async_tick_expenses(tg_chat.chat_id, duration, model)
    return response.text