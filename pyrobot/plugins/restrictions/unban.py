from pyrogram import Client, filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.admin_check import admin_check
from pyrobot.helper_functions.extract_user import extract_user


@Client.on_message(filters.command(["unban", "unmute"], COMMAND_HAND_LER))
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Okay, changed ... now "
                f"{user_first_name} Can "
                " Join the Group Again!"
            )
        else:
            await message.reply_text(
                "Ok Changed Now"
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> Can "
                "Join The Group Again!"
            )
