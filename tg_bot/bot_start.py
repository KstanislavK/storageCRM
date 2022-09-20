from aiogram.utils import executor
from bot_create import dp


async def on_startup(_):
    print('[INFO] -> Bpt started')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
