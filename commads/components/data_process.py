from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from .user import UserInfo
from .language import Language
from .memory import Form

def crea_mecard(data):
    name = data['title']
    surname = data['surname']
    caselle = data['caselle']

    mecard = f"MECARD:N:{name},{surname};"
    for casella in caselle:
        mecard += f"URL:{casella['url']};EMAIL:{casella['email']};TEL:{casella['phone']};"
    return mecard

def crea_wifi(data):
    name = data['name']
    password = data['password']
    wifi = f"WIFI:T:WPA;S:{name};P:{password};;"
    return wifi

async def wait_user_prompt(message: Message, state: FSMContext):
    info = UserInfo(message)
    user_id = info.user_id
    language_text = Language()
    language_code = info.language
    status = await info.get_vip_member(user_id)
    send_me_prompt = language_text.send_prompt(language_code)
    await message.reply(send_me_prompt)
    await state.set_state(Form.set_prompt)