import openai
import io
import json
from pydub import AudioSegment

from main import *
from commandHandlers import start
from serviceHelpers import check_is_chat_approved
from DatabaseHelpers.DMLHelpers import tick_expenses


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
                                       text=f"""Recognized text: {recognized_text}

        Processing, please wait...""")

        #json_update = json.loads(update.to_json())
        #json_update = audio_json_to_text(json_update, recognized_text)
        #print('audio_json_to_text')
        #new_update = Update.de_json(json_update, context)
        #await chat_gpt_message(new_update, context)


async def process_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_message = await context.bot.get_file(update.message.voice.file_id)
    mem_file = io.BytesIO()
    await voice_message.download_to_memory(mem_file)
    mem_file.seek(0)
    ogg_audio = AudioSegment.from_file(mem_file, format="ogg")

    # Convert the audio file to wav format
    ogg_audio.export(mem_file, format="wav")
    duration = ogg_audio.duration_seconds
    mem_file.seek(0)
    mem_file.name = f'voice_{update.message.chat_id}_{update.message.message_id}.wav'
    return mem_file, duration


async def voice_to_text(chat, voice_file, duration: float):
    print(duration)
    openai.api_key = secrets['OPENAI_API']
    model = "whisper-1" # there is no other model
    response = openai.Audio.transcribe(model, voice_file)
    await tick_expenses(chat, duration, model)
    return response.text
