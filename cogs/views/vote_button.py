import re
from typing import Tuple, Self

import discord

from utils.bug_vote_controller import BugVoteController

from utils.suggestion_vote_controller import SuggestionVoteController
from utils.vote_controller import VoteController


class VoteButton(
    discord.ui.DynamicItem[discord.ui.Button],
    template=r'user:(?P<uid>[0-9]+):type:(?P<type>[0-9]+)',
):
    def __init__(self, owner_id: int, users: list, vote_type: int, report_id: int):
        self.users, self.owner_id, self.count = users, owner_id, len(users)
        self.controller = resolve_type(owner_id, vote_type)
        self.report_id = report_id
        super().__init__(
            discord.ui.Button(
                label=self.controller.get_title(),
                style=self.style,
                custom_id=f'user:{self.owner_id}:type:{vote_type}',
                emoji=self.controller.get_emoji(),
            )
        )
    
    @property
    def style(self) -> discord.ButtonStyle:
        return self.controller.get_style()

    @classmethod
    async def from_custom_id(cls, interaction: discord.Interaction, item: discord.ui.Button, match: re.Match[str], /):
        owner_id = int(match.group("uid"))
        vote_type = int(match.group("type"))
        controller = resolve_type(owner_id, vote_type)
        report_id = interaction.message.embeds[0].title.split('#')[-1].strip()
        user_ids = await controller.get_user_votes(report_id)
        return cls(owner_id, user_ids, vote_type, report_id)

    @classmethod
    async def initialize(cls, owner_id, users, vote_type, message_id: int) -> Tuple[Self, int]:
        controller = resolve_type(owner_id, vote_type)
        report_id = await controller.initialize(message_id)
        view = cls(owner_id, users, vote_type, report_id)
        return view, report_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id == self.owner_id:
            await interaction.response.send_message("You are not allowed to use this button.", ephemeral=True)
            return False
        return True

    async def callback(self, interaction: discord.Interaction) -> None:
        submittal_title = interaction.message.embeds[0].description.split('\n')[0].strip()
        self.controller.log_user_vote(interaction.user, submittal_title)
        await self.populate_vals_if_empty(self.report_id)
        if interaction.user.id in self.users:
            self.users.remove(interaction.user.id)
            await self.controller.remove_user_vote(self.report_id, interaction.user.id)
            self.count -= 1
        else:
            self.users.append(interaction.user.id)
            await self.controller.add_user_vote(self.report_id, interaction.user.id)
            self.count += 1

        message = self.get_message()
        embed = interaction.message.embeds[0]
        embed.set_footer(text=message)

        await interaction.response.edit_message(embed=embed, view=self.view)

    def get_message(self) -> str:
        return self.controller.message_gen(self.count)

    async def populate_vals_if_empty(self, report_id: int) -> None:
        if len(self.users) == 0:
            self.users = await self.controller.get_user_votes(report_id)
            self.count = len(self.users)


def resolve_type(owner_id, vote_type: int) -> VoteController | None:
    match vote_type:
        case 0:
            return BugVoteController(owner_id)
        case 1:
            return SuggestionVoteController(owner_id)
    return None
