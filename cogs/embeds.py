import discord
from discord.ext import commands

from lib.config import queue_reactions, session_reactions, power_levels, life_levels, life_emoji, rule_url


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def queue(inst, url):
        embed = discord.Embed(type='rich', colour=0x79edf7)
        embed.set_author(name='The Mind: Queue', url=f'{rule_url}', icon_url=url)
        footer_array = [queue_reactions[reaction].get_arg_str() for reaction in queue_reactions]
        footer = ', '.join(footer_array)
        embed.set_footer(text=f'{footer}')

        for player in inst.players:
            embed.add_field(name=f'Player {player.number}', value=player.user.mention, inline=False)

        return embed

    @staticmethod
    def session(inst, url):
        embed = discord.Embed(
            description=f'Lives: {inst.lives}{life_emoji}, Powers: {inst.powers}{session_reactions["power"].name}',
            type='rich', colour=0x79edf7)
        embed.set_author(name=f'The Mind: Level #{inst.level}', url=f'{rule_url}', icon_url=url)
        footer_array = [session_reactions[reaction].get_arg_str() for reaction in session_reactions]
        footer = ', '.join(footer_array)
        embed.set_footer(text=f'{footer}')

        for player in inst.players:
            hand = ', '.join(player.hand_array)
            hidden_hand = f'||{hand}||'

            if not player.hand_array:
                hidden_hand = 'All cards played.'

            if player.power_array:
                lowest = ', '.join(player.power_array)
                hidden_hand = f'{hidden_hand} Former lowest: {lowest}'

            embed.add_field(name=f'Player {player.number}: {player.user.display_name}#{player.user.discriminator}',
                            value=f'{hidden_hand}', inline=False)

        table = ', '.join(inst.table_array)
        if not table:
            table = 'No cards played yet.'
        embed.add_field(name='Table', value=f'{table}', inline=False)

        return embed

    @staticmethod
    def advance(inst, url):
        embed = Embeds.session(inst, url)
        advance_text = 'Advancing to the next level...'

        if inst.level in power_levels:
            advance_text = f'1 Power gained. {advance_text}'

        if inst.level in life_levels:
            advance_text = f'1 Life gained. {advance_text}'

        embed.add_field(name=f'Level #{inst.level} passed.', value=f'{advance_text}', inline=False)
        return embed

    @staticmethod
    def revert(inst, url):
        embed = Embeds.session(inst, url)
        embed.add_field(name=f'Level #{inst.level} failed.', value='1 Life lost, retrying level...', inline=False)
        return embed

    @staticmethod
    def reset(inst, url):
        embed = Embeds.session(inst, url)
        embed.set_field_at(index=len(inst.players), name='Table', value='**Timing reset! Prepare to continue...**',
                           inline=False)
        return embed

    @staticmethod
    def terminate(inst, url):
        embed = Embeds.session(inst, url)
        embed.add_field(name=f'Level #{inst.level} failed.', value='All lives lost, terminating...', inline=False)
        return embed

    @staticmethod
    def results(inst, url):
        embed = discord.Embed(type='rich', colour=0x79edf7)
        embed.set_author(name='The Mind: Results', url=f'{rule_url}', icon_url=url)
        player_array = [player.user.mention for player in inst.players]
        players = ', '.join(player_array)
        embed.add_field(name=f'Players:', value=players, inline=False)
        embed.add_field(name=f'Max level reached: ', value=inst.max_level, inline=False)

        return embed

    def choose_embed(self, inst):
        actions = {
            'queue': self.queue,
            'session': self.session,
            'advance': self.advance,
            'revert': self.revert,
            'reset': self.reset,
            'terminate': self.terminate,
            'results': self.results
        }

        url = self.bot.user.avatar_url
        embed = actions[inst.state](inst, url)

        return embed

    # scores
    def scores(self, user, score_dict):
        url = self.bot.user.avatar_url

        embed = discord.Embed(type='rich', colour=0x79edf7)
        embed.set_author(name='The Mind: Scores', url=f'{rule_url}', icon_url=url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Player:', value=user.mention, inline=False)

        print(score_dict)

        for key, score in score_dict.items():
            embed.add_field(name=f'{key}:'.replace('_', ' ').capitalize(), value=f'{score}', inline=True)

        return embed


def setup(bot):
    bot.add_cog(Embeds(bot))
