
import discord
from discord.ext import commands, tasks


class BackgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_count_channel = discord.Object(1374399695195213965)
        self.auto_role = discord.Object(1373542685243080704)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(self.member_count_channel.id)
        if channel is None:
            return

        await channel.edit(name=f"Tester Count: {member.guild.member_count}")
        await member.add_roles(self.auto_role)


async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot))
    print(f'Loaded cog: {BackgroundTasks.__name__}')
