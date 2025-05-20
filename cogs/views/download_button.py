import discord


class GithubReleaseDownload(discord.ui.View):
    def __init__(self, link):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Download Version", url=link, style=discord.ButtonStyle.url))
