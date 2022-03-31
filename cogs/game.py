from discord.ext import commands
import random

import lib.config as config


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    instances = []

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        Embeds = self.bot.get_cog('Embeds')

        inst = self.Instance(ctx.author)
        self.instances.append(inst)
        embed = Embeds.choose_embed(inst)

        message = await ctx.send(embed=embed)
        inst.add_ctx(await self.bot.get_context(message))

        for reaction in config.queue_reactions:
            await message.add_reaction(config.queue_reactions[reaction].name)

    class Instance:
        def __init__(self, host):
            self.ctx = None
            self.players = list()
            self.player_index = 1
            self.add_player(host)
            self.table_array = list()
            self.state = 'queue'
            self.level = 1
            self.max_level = 1
            self.level_cards = list()
            self.powers = 1
            self.lives = None

        def add_ctx(self, ctx):
            self.ctx = ctx

        def add_player(self, user):
            player = Game.Instance.Player(self, user)
            self.players.append(player)

        def cards(self, level):
            cardpool = [f'{i:0>2d}' for i in range(1, 100)]  # The Mind has cards from 01 to 99
            self.level_cards = random.sample(cardpool, len(self.players) * level)
            print(self.level_cards)

            for player in self.players:
                player.hand_array = self.level_cards[(player.number - 1) * level: player.number * level]
                player.hand_array.sort()
                print(player.hand_array)

            self.level_cards.sort()

            return

        def clear_cards(self):
            for player in self.players:
                player.hand_array = list()
                player.power_array = list()
            self.table_array = list()
            return

        class Player:
            def __init__(self, inst, user):
                self.user = user
                self.number = inst.player_index
                self.hand_array = list()
                self.power_array = list()
                inst.player_index += 1

    @staticmethod
    async def initiate_session(inst):
        inst.state = 'session'
        message = inst.ctx.message
        await message.clear_reactions()

        for reaction in config.session_reactions:
            await message.add_reaction(config.session_reactions[reaction].name)

        inst.lives = len(inst.players)
        inst.cards(inst.level)

        return

    @staticmethod
    def temp_session(inst):
        if inst.state == 'reset':
            return

        inst.clear_cards()

        if inst.state == 'advance':
            if inst.level in config.power_levels:
                inst.powers += 1

            if inst.level in config.life_levels:
                inst.lives += 1
            inst.level += 1

        if inst.state == 'terminate':
            inst.state = 'results'

        inst.cards(inst.level)

        inst.max_level = inst.level if inst.level > inst.max_level else inst.max_level

        return


def setup(bot):
    bot.add_cog(Game(bot))
