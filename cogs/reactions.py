import time

import discord.errors
from discord.ext import commands

import lib.config as config


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def action_handling(self, inst, user, emoji_name):
        Game = self.bot.get_cog('Game')
        Embeds = self.bot.get_cog('Embeds')
        Scores = self.bot.get_cog('Scores')

        if inst:
            if any(player for player in inst.players if user == player.user) or emoji_name == config.queue_reactions['join'].name:

                self.choose_action(emoji_name, inst, user=user)

                if inst.state == 'queue' and len(inst.players) > 1 and emoji_name == config.queue_reactions['start'].name:
                    await Game.initiate_session(inst)

                if not inst.players:
                    Game.instances.remove(inst)

                    await inst.ctx.message.delete()

                    return

                if inst.state in config.temp_states:
                    embed = Embeds.choose_embed(inst)
                    Game.temp_session(inst)

                    await inst.ctx.message.edit(embed=embed)

                    if not inst.state == 'results':
                        inst.state = 'session'

                    time.sleep(config.temp_time)

                embed = Embeds.choose_embed(inst)
                await inst.ctx.message.edit(embed=embed)

                if inst.state == 'results':
                    Game.instances.remove(inst)
                    for player in inst.players:
                        Scores.update_score(player.user, inst.max_level)

                    await inst.ctx.message.clear_reactions()

                    return

        return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        Game = self.bot.get_cog('Game')
        Errors = self.bot.get_cog('Errors')

        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = payload.member
        emoji_name = payload.emoji.name

        if user.bot:
            return

        inst = next((inst for inst in Game.instances if inst.ctx.message == message), None)

        await self.action_handling(inst, user, emoji_name)

        if inst:
            try:
                await message.remove_reaction(emoji_name, user)
            except discord.errors.NotFound:
                await Errors.choose_error('reaction_not_found')

        return

    # queue
    @staticmethod
    def join(inst, user):
        if not (len(inst.players) >= config.maxplayers or any(user for player in inst.players if user == player.user)):
            inst.add_player(user)
        return

    @staticmethod
    def leave(inst, user):
        leaving_user = next(player for player in inst.players if user == player.user)
        inst.players.remove(leaving_user)
        return

    @staticmethod
    def start(inst, user):
        return

    @staticmethod
    def stop(inst):
        inst.players.clear()
        return

    # session
    @staticmethod
    def play(inst, user):
        player = next(player for player in inst.players if user == player.user)

        if not player.hand_array:
            return

        played_card = player.hand_array[0]
        right_card = inst.level_cards[0]

        print(f'{played_card}, {right_card}')

        if played_card == right_card:
            print('right card played')
            inst.level_cards.remove(played_card)

            if not inst.level_cards:
                inst.state = 'advance'

        else:
            print('wrong card played')
            inst.lives -= 1
            inst.state = 'revert'

            if inst.lives == 0:
                inst.state = 'terminate'

        player.hand_array.remove(played_card)
        inst.table_array.append(played_card)

        return

    @staticmethod
    def power(inst):
        if inst.powers == 0:
            return

        inst.powers -= 1

        powerable_players = [player for player in inst.players if player.hand_array]

        for player in powerable_players:
            lowest = player.hand_array[0]
            player.power_array.append(lowest)
            player.hand_array.remove(lowest)
            inst.level_cards.remove(lowest)

        if not inst.level_cards:
            inst.state = 'advance'

        return

    @staticmethod
    def reset(inst):
        inst.state = 'reset'
        return

    @staticmethod
    def terminate(inst):
        inst.state = 'results'
        return

    # action picker
    @staticmethod
    def choose_action(emoji_name, inst, **kwargs):
        if inst.state == 'session':
            reactions = config.session_reactions

            actions = {
                reactions['play'].name: Reactions.play,
                reactions['reset'].name: Reactions.reset,
                reactions['power'].name: Reactions.power,
                reactions['terminate'].name: Reactions.terminate

            }

        else:
            reactions = config.queue_reactions

            actions = {
                reactions['join'].name: Reactions.join,
                reactions['leave'].name: Reactions.leave,
                reactions['start'].name: Reactions.start,
                reactions['stop'].name: Reactions.stop
            }

        if any(emoji for emoji in reactions if reactions[emoji].has_kwargs and reactions[emoji].name == emoji_name):
            actions[emoji_name](inst, kwargs['user'])
        else:
            actions[emoji_name](inst)
        return


def setup(bot):
    bot.add_cog(Reactions(bot))
