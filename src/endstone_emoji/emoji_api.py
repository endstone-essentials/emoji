import json

from endstone import Player
from endstone.util import Vector
from endstone.network import SpawnParticleEffectPacket


class EmojiAPI:
    EMOJI_POS: dict[str, list[float]] = {
        "smiley": [0, 0],
        "grimacing": [0.01, 0],
        "grin": [0.02, 0],
        "joy": [0.03, 0],
        "smile": [0.04, 0],
        "sweat_smile": [0.05, 0],
        "laughing": [0.06, 0],
        "innocent": [0.07, 0],
        "wink": [0, 0.01],
        "blush": [0.01, 0.01],
        "slight_smile": [0.02, 0.01],
        "upside_down": [0.03, 0.01],
        "relaxed": [0.04, 0.01],
        "yum": [0.05, 0.01],
        "relieved": [0.06, 0.01],
        "heart_eyes": [0.07, 0.01],
        "kissing_heart": [0, 0.02],
        "kissing": [0.01, 0.02],
        "kissing_smiling_eyes": [0.02, 0.02],
        "kissing_closed_eyes": [0.03, 0.02],
        "stuck_out_tongue_winking_eye": [0.04, 0.02],
        "stuck_out_tongue_closed_eyes": [0.05, 0.02],
        "stuck_out_tongue": [0.06, 0.02],
        "money_mouth": [0.07, 0.02],
        "sunglasses": [0, 0.03],
        "smirk": [0.01, 0.03],
        "no_mouth": [0.02, 0.03],
        "neutral_face": [0.03, 0.03],
        "expressionless": [0.04, 0.03],
        "unamused": [0.05, 0.03],
        "rolling_eyes": [0.06, 0.03],
        "flushed": [0.07, 0.03],
        "disappointed": [0, 0.04],
        "worried": [0.01, 0.04],
        "angry": [0.02, 0.04],
        "rage": [0.03, 0.04],
        "pensive": [0.04, 0.04],
        "confused": [0.05, 0.04],
        "slight_frown": [0.06, 0.04],
        "frowning2": [0.07, 0.04],
    }

    def __init__(self, plugin):
        self.plugin = plugin
        self.emoji_names: dict[str, str] = plugin.config["emoji-names"]
        self.emoji_phrases: dict[str, list[str]] = plugin.config["emoji-phrases"]

    def send_emoji(self, player: Player, emoji_id: str):
        if emoji_id not in self.emoji_names:
            return

        pos: list[float] = EmojiAPI.EMOJI_POS[emoji_id]

        packet = SpawnParticleEffectPacket()
        packet.dimension_id = int(player.dimension.type)
        packet.actor_id = -1
        packet.position = player.location + Vector(0, 2.5, 0)
        packet.effect_name = "emoji:emoji"
        packet.molang_variables_json = json.dumps(
            [
                {"name": "variable.ix", "value": {"type": "float", "value": pos[0]}},
                {"name": "variable.iy", "value": {"type": "float", "value": pos[1]}},
            ]
        )

        for online_player in player.server.online_players:
            if online_player.dimension.type != player.dimension.type:
                return
            online_player.send_packet(packet)

    def get_phrase_emoji(self, text: str) -> str | None:
        text = text.lower()
        for emoji_id, phrases in self.emoji_phrases.items():
            for phrase in phrases:
                if phrase in text:
                    return emoji_id
        return None
