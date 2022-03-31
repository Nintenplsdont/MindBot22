# change automatic cog loading in main file with checking if __name__ is __main__

from discord.ext import commands
import os

from lib.config import bot, game, admin_ids


# Basic
@bot.event
async def on_ready():
    print(f'Logged on as {format(bot.user)}!')
    await bot.change_presence(activity=game)


@bot.command()
async def ping(ctx):
    await ctx.send('Pong.')


# File Handling
def is_admin(ctx):
    if ctx.author.id in admin_ids:
        return True
    return False


@bot.command()
async def load(ctx, extension):
    Errors = bot.get_cog('Errors')
    if not is_admin(ctx):
        return

    if extension == 'all':
        all_cogs('load')
        await ctx.send('All cogs loaded.')

    else:
        try:
            bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'``{extension}`` loaded.'.capitalize())

        except commands.errors.ExtensionNotFound:
            await Errors.choose_error('ext_not_found', ctx=ctx, extension=extension)

        except commands.errors.ExtensionAlreadyLoaded:
            await Errors.choose_error('ext_already_loaded', ctx=ctx, extension=extension)


@bot.command()
async def unload(ctx, extension):
    Errors = bot.get_cog('Errors')
    if not is_admin(ctx):
        return

    if extension == 'all':
        all_cogs('unload')
        await ctx.send('All cogs unloaded.')

    else:
        try:
            bot.unload_extension(f'cogs.{extension}')
            await ctx.send(f'``{extension}`` unloaded.'.capitalize())

        except commands.errors.ExtensionNotFound:
            await Errors.choose_error('ext_not_found', ctx=ctx,  extension=extension)

        except commands.errors.ExtensionNotLoaded:
            await Errors.choose_error('ext_not_loaded', ctx=ctx, extension=extension)


@bot.command()
async def reload(ctx, extension):
    Errors = bot.get_cog('Errors')
    if not is_admin(ctx):
        return

    if extension == 'all':
        all_cogs('reload')
        await ctx.send('All cogs reloaded.')

    else:
        try:
            bot.unload_extension(f'cogs.{extension}')
            bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'``{extension}`` reloaded.'.capitalize())

        except commands.errors.ExtensionNotFound:
            await Errors.choose_error('ext_not_found', ctx=ctx, extension=extension)

        except commands.errors.ExtensionNotLoaded:
            await Errors.choose_error('ext_not_loaded', ctx=ctx, extension=extension)


def all_cogs(action):
    cogfiles = [filename for filename in os.listdir('./cogs') if filename.endswith('.py')]
    actions = dict(load=load_all, unload=unload_all, reload=reload_all)
    actions[action](cogfiles)


def load_all(cogfiles):
    for cog_filename in cogfiles:
        bot.load_extension(f'cogs.{cog_filename[:-3]}')
    return


def unload_all(cogfiles):
    for cog_filename in cogfiles:
        bot.unload_extension(f'cogs.{cog_filename[:-3]}')
    return


def reload_all(cogfiles):
    unload_all(cogfiles)
    load_all(cogfiles)
    return


all_cogs('load')


bot.run('token')
