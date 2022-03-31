import discord
from discord.ext import commands

admin_ids = [368735410043486209]
rule_url = 'https://nsv-spiele.de/wp-content/uploads/2020/06/TheMind_GB.pdf'

prefix = 'mib '
bot = commands.Bot(command_prefix=prefix)
game = discord.Game(f'The Mind | {prefix}')

maxplayers = 4
temp_time = 2
temp_states = ['advance', 'revert', 'reset', 'terminate']

power_levels = [2, 5, 8]
life_levels = [3, 6, 9]
life_emoji = '💙'


class Reaction:
    def __init__(self, name, has_kwargs, desc):
        self.has_kwargs = has_kwargs
        self.name = name
        self.desc = desc

    def get_arg_str(self):
        arg_str = f'{self.name} {self.desc}'
        return arg_str


join = Reaction('✅', True, ' to join')
leave = Reaction('❌', True, ' to leave')
start = Reaction('▶', True, ' to start game')
stop = Reaction('⏹', False, 'to stop queue')

play = Reaction('☄', True, ' to play lowest card')
reset = Reaction('⌛', False, 'to signal timing reset')
power = Reaction('⚡', False, 'to use power')
terminate = Reaction('🛑', False, 'to end game')

queue_reactions = {
    'join': join,
    'leave': leave,
    'start': start,
    'stop': stop
}

session_reactions = {
    'play': play,
    'reset': reset,
    'power': power,
    'terminate': terminate
}
