from endstone import Player
from endstone.form import ActionForm
from endstone.command import Command, CommandSender
from endstone.event import PlayerChatEvent, event_handler
from endstone.plugin import Plugin

from endstone_emoji.emoji_api import EmojiAPI


class EmojiPlugin(Plugin):
    api_version = "0.5"

    commands = {
        "emoji": {
            "description": "Send a emoji",
            "usages": ["/emoji"],
            "aliases": ["emj", "ej"],
            "permissions": ["emoji.command.emoji"],
        },
    }

    permissions = {
        "emoji.command": {
            "description": "Allow users to use all commands provided by this plugin.",
            "default": True,
            "children": {
                "emoji.command.emoji": True,
            },
        },
        "emoji.command.emoji": {
            "description": "Allow users to use the /emoji command.",
            "default": True,
        },
    }

    def __init__(self):
        super().__init__()
        self.emoji_api: EmojiAPI | None = None

    def on_enable(self) -> None:
        self.save_default_config()
        self.emoji_api = EmojiAPI(self)
        self.register_events(self)

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_error_message("This command can only be executed by player")
            return False

        form = ActionForm("§fEmoji")
        form.content = "§bChoose the emoji you want!"

        for k, v in self.emoji_api.emoji_names.items():
            form.add_button(
                text=f"§f{v}§8\n{k}",
                on_click=lambda player: self.emoji_api.send_emoji(player, k)
            )

        sender.send_form(form)

        return True

    @event_handler()
    def on_chat(self, event: PlayerChatEvent):
        if not self.config["auto-emoji"]:
            return

        emoji_id = self.emoji_api.get_phrase_emoji(event.message)

        if emoji_id is None:
            return

        self.emoji_api.send_emoji(
            event.player,
            emoji_id
        )
