import json
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup
)
from pyrobot import (
    COMMAND_HAND_LER,
    TG_URI,
    TG_IRU_S_M_ID
)
from pyrobot.pyrobot import PyroBot
from pyrobot.helper_functions.cust_p_filters import admin_fliter
from pyrobot.helper_functions.msg_types import (
    get_note_type,
    Types
)


@PyroBot.on_message(
    filters.command(["savefilter", "filter"], COMMAND_HAND_LER) &
    admin_fliter
)
async def save_filter(client: PyroBot, message):
    status_message = await message.reply_text(
        "Wait a Sec",
        quote=True
    )
    if (
        message.reply_to_message and
        message.reply_to_message.reply_markup is not None
    ):
        fwded_mesg = await message.reply_to_message.forward(
            chat_id=TG_URI,
            disable_notification=True
        )
        chat_id = message.chat.id
        filter_kw = " ".join(message.command[1:])
        fm_id = fwded_mesg.message_id

        client.filterstore[str(chat_id)][filter_kw] = fm_id
        await client.save_public_store(
            TG_IRU_S_M_ID,
            json.dumps(client.filterstore)
        )

        await status_message.edit_text(
            f"filter <u>{filter_kw}</u> added"
            # f"<a href='https://'>{message.chat.title}</a>"
        )

    else:
        filter_kw, text, data_type, content, buttons = get_note_type(
            message,
            2
        )

        if data_type is None:
            await status_message.edit_text("🤔 Note Text is empty")
            return

        if not filter_kw:
            await status_message.edit_text(
                "It is Not Clear 🤔"
            )
            return

        # construct message using the above parameters
        fwded_mesg = None
        reply_markup = None
        if len(buttons) > 0:
            reply_markup = InlineKeyboardMarkup(buttons)
        if data_type in (Types.BUTTON_TEXT, Types.TEXT):
            fwded_mesg = await client.send_message(
                chat_id=TG_URI,
                text=text,
                parse_mode="md",
                disable_web_page_preview=True,
                disable_notification=True,
                reply_to_message_id=1,
                reply_markup=reply_markup
            )
        elif data_type is not None:
            fwded_mesg = await client.send_cached_media(
                chat_id=TG_URI,
                file_id=content,
                caption=text,
                parse_mode="md",
                disable_notification=True,
                reply_to_message_id=1,
                reply_markup=reply_markup
            )

        # save to db 🤔
        if fwded_mesg is not None:
            chat_id = message.chat.id
            fm_id = fwded_mesg.message_id

            client.filterstore[str(chat_id)][filter_kw] = fm_id
            await client.save_public_store(
                TG_IRU_S_M_ID,
                json.dumps(client.filterstore)
            )

            await status_message.edit_text(
                f"Filter <u>{filter_kw}</u> Added Successfully"
                # f"<a href='https://'>{message.chat.title}</a>"
            )
        else:
            await status_message.edit_text("🥺 This Might Be an Error 🤔")
