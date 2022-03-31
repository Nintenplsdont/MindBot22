from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Cog Loading
    @staticmethod
    def ext_not_found(extension):
        error = f'There is no cog called ``{extension}``.'
        return error

    @staticmethod
    def ext_already_loaded(extension):
        error = f'``{extension}`` is already loaded.'
        return error

    @staticmethod
    def ext_not_loaded(extension):
        error = f'``{extension}`` is not loaded.'
        return error

    # Game
    @staticmethod
    def reaction_not_found():
        error = 'Reaction not found, message might have been deleted already.'
        return error

    # Error Picker
    async def choose_error(self, errortype, **kwargs):
        errors = {
            'ext_not_found': self.ext_not_found,
            'ext_already_loaded': self.ext_already_loaded,
            'ext_not_loaded': self.ext_not_loaded,
            'reaction_not_found': self.reaction_not_found
        }

        if not kwargs:
            error = errors[errortype]()
            print(error)
            return

        else:
            error = None

        if kwargs['extension']:
            error = errors[errortype](kwargs['extension'])

        if kwargs['ctx']:
            await kwargs['ctx'].send(error)


def setup(bot):
    bot.add_cog(Errors(bot))
