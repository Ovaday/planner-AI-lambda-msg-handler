from DatabaseHelpers.QueryHelpers import async_get_users_by_role


async def send_all_admins(db_connection, context, message, reply_markup=None):
    admins = await async_get_users_by_role(db_connection, 'admin')
    for admin in admins:
        await context.bot.send_message(chat_id=admin.chat_id, text=message, reply_markup=reply_markup)


async def message_specific(chat_id, application, message, reply_markup=None):
    await application.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)