import telegram
from functools import cached_property

from utils.ArgParser import ArgParser
from handlers.VideoHandler import VideoHandler


class TelegramHandler(ArgParser, VideoHandler):
    def _add_parser_args(self, parser):
        super()._add_parser_args(parser)
        # parser.add_argument(
        #     "TOKEN",
        #     type=str,
        #     help=f"Provide Telegram Token to access to the API",
        # )
        # parser.add_argument(
        #     "CHAT_ID",
        #     type=str,
        #     help=f"Provide Telegram CHAT ID",
        # )

    @cached_property
    def chat_id(self):
        return int(self.args.chat_id)

    def __int__(self):
        ArgParser.__init__(self, prog="TelegramSecurityBot")
        VideoHandler.__init__()
        self.bot = telegram.Bot(self.args.token, use_context=True)

    async def senf_video(self):
        self.save_video()
        with open(self.os.path.join(self.video_path, "move_detected.mp4"), "rb") as fd:
            v = fd.read()
        async with self.bot:
            await self.bot.send_video(chat_id=self.chat_id, video=v, supports_streaming=True, caption="Movement detected in your room")
