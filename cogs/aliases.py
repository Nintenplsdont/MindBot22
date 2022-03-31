from discord.ext import commands
from lib.config import queue_reactions
from lib.config import session_reactions


class Aliases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def alias_handling(self, ctx, emoji_name):
        Game = self.bot.get_cog('Game')
        Reactions = self.bot.get_cog('Reactions')

        user = ctx.author
        inst = next((inst for inst in reversed(Game.instances) if inst.ctx.channel == ctx.channel), None)
        await Reactions.action_handling(inst, user, emoji_name)
        await ctx.message.delete()

    # queue
    @commands.command(aliases=['j'])
    async def join(self, ctx):
        emoji_name = queue_reactions['join'].name
        await self.alias_handling(ctx, emoji_name)
        return

    @commands.command(aliases=['l, quit'])
    async def leave(self, ctx):
        emoji_name = queue_reactions['leave'].name
        await self.alias_handling(ctx, emoji_name)
        return

    @commands.command(aliases=['begin', 'initiate', 'init'])
    async def start(self, ctx):
        emoji_name = queue_reactions['start'].name
        await self.alias_handling(ctx, emoji_name)
        return

    @commands.command(aliases=['end'])
    async def stop(self, ctx):
        emoji_name = queue_reactions['stop'].name
        await self.alias_handling(ctx, emoji_name)
        return

    # session
    @commands.command(aliases=['p'])
    async def play(self, ctx):
        emoji_name = session_reactions['play'].name
        await self.alias_handling(ctx, emoji_name)
        return

    @commands.command(aliases=['r'])
    async def reset(self, ctx):
        emoji_name = session_reactions['reset'].name
        await self.alias_handling(ctx, emoji_name)
        return

    @commands.command(aliases=['pow'])
    async def power(self, ctx):
        emoji_name = session_reactions['power'].name
        await self.alias_handling(ctx, emoji_name)
        return

    @commands.command()
    async def terminate(self, ctx):
        emoji_name = session_reactions['terminate'].name
        await self.alias_handling(ctx, emoji_name)
        return


def setup(bot):
    bot.add_cog(Aliases(bot))
