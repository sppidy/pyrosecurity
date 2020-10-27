import json
from pyrogram import filters
from pyrobot import (
    COMMAND_HAND_LER,
    MAX_MESSAGE_LENGTH,
    TG_IRU_S_M_ID
)
from pyrobot.pyrobot import PyroBot
from pyrobot.helper_functions.cust_p_filters import admin_fliter


@PyroBot.on_message(
    filters.command(["clearfilter"], COMMAND_HAND_LER) &
    admin_fliter
)
async def clear_filter(client: PyroBot, message):
    status_message = await message.reply_text(
        "Wait a Sec",
        quote=True
    )
    flt_name = " ".join(message.command[1:])
    flt_list = client.filterstore.get(str(message.chat.id), [])
    flt_list.pop(flt_name)
    await client.save_public_store(
        TG_IRU_S_M_ID,
        json.dumps(client.filterstore)
    )
    await status_message.edit_text(
        f"filter <u>{flt_name}</u> Deleted from current chat."
    )


@PyroBot.on_message(
    filters.command(["listfilters", "filters"], COMMAND_HAND_LER)
)
async def list_filters(client: PyroBot, message):
    status_message = await message.reply_text(
        "Wait a Sec..",
        quote=True
    )
    flt_list = client.filterstore.get(str(message.chat.id), [])
    msg = "<b>Filters in {}:</b>\n".format("the current chat")
    msg_p = msg
    for flt in flt_list:
        flt_name = " - <code>{}</code>\n".format(flt)
        if len(msg) + len(flt_name) > MAX_MESSAGE_LENGTH:
            await message.reply_text(msg)
            msg = ""
        msg += f"{flt_name}"
    if msg == msg_p:
        await status_message.edit_text("No Notes Found In this Chat")

    elif len(msg) != 0:
        await message.reply_text(msg)
        await status_message.delete()
