from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import increment


class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Player = Query()
        self.db = TinyDB('scores/scores.json')

    # db handling
    def insert_score(self, user, new_max_level):
        self.db.insert({'id': f'{user.id}', 'max_level_reached': new_max_level, 'games_played': 0})

    def get_score(self, user):
        user_id = f'{user.id}'
        user_dict = self.db.get(self.Player.id == user_id)

        if not user_dict:
            self.insert_score(user, 1)
            user_dict = self.db.get(self.Player.id == user_id)

        return user_dict

    def update_score(self, user, new_max_level):
        user_id = f'{user.id}'

        if self.get_score(user):
            self.db.update(increment('games_played'), (self.Player.id == user_id))
            self.db.update({'max_level_reached': new_max_level},
                           (self.Player.id == user_id) & (self.Player.max_level_reached < new_max_level))

        else:
            self.insert_score(user, new_max_level)

    # db interaction
    @commands.command()
    async def scores(self, ctx):
        Embeds = self.bot.get_cog('Embeds')

        user = ctx.message.mentions[0]

        if user.bot:
            return

        user_dict = self.get_score(user)

        score_dict = {key: user_dict[key] for key in user_dict if key != 'id'}
        embed = Embeds.scores(user, score_dict)

        await ctx.send(embed=embed)

        return


def setup(bot):
    bot.add_cog(Scores(bot))
