import copy
import re

import discord
from discord.app_commands import private_channel_only

from utils.bot_logging import log_message


class SuggestionVoteDynamicItem(
    discord.ui.DynamicItem[discord.ui.Button],
    template=r'suggestionbutton:(?P<id>(\d*,?)*)?:user:(?P<uid>[0-9]+)'
):
    def __init__(self, user_id: int, message: str, users: list, emoji: str = None):
        self.users = users
        self.user_id = user_id
        self.emoji = emoji
        self.message = message
        self.count = len(self.users)
        super().__init__(
            discord.ui.Button(
                label=self.message,
                style=self.style,
                custom_id=f'suggestionbutton:{",".join(map(str, self.users))}:user:{self.user_id}',
                emoji=self.emoji,
            )
        )

    @property
    def style(self) -> discord.ButtonStyle:
        return discord.ButtonStyle.green

    @classmethod
    async def from_custom_id(cls, interaction: discord.Interaction, item: discord.ui.Button, match: re.Match[str], /):
        user_ids_str = match.group("id")
        user_id = int(match.group("uid"))
        user_ids = user_ids_str.split(',') if user_ids_str else []
        emoji = '⬆️'
        message = 'Suggest Feature'
        return cls(user_id, message, user_ids, emoji)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id == self.user_id:
            await interaction.response.send_message("You are not allowed to use this button.", ephemeral=True)
            return False
        return True

    async def callback(self, interaction: discord.Interaction) -> None:
        first_line = interaction.message.embeds[0].description.split('\n')[0]
        log_message(f"{interaction.user.name} has interacted with feature suggest button\n{first_line}")
        if str(interaction.user.id) in self.users:
            self.users.remove(str(interaction.user.id))
            self.count -= 1
        else:
            self.users.append(str(interaction.user.id))
            self.count += 1

        self.custom_id = f'suggestionbutton:{",".join(map(str, self.users))}:user:{self.user_id}'
        self.item.style = self.style
        message = message_gen(self.users)
        embed = interaction.message.embeds[0]
        embed.set_footer(text=message)
        view = discord.ui.View()
        view.add_item(
            SuggestionVoteDynamicItem(
                self.user_id,
                "Suggest Feature",
                self.users,
                self.emoji
            )
        )

        await interaction.response.edit_message(embed=embed, view=view)




def message_gen(users: list) -> str:
    return '1 person is requesting this feature.' if len(users) == 1 else (f'{len(users)} '
                                                                        f'people are requesting this feature.')
