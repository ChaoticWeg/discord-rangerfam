from discord.ext import commands

class WegbotCommandError(commands.CommandError):
    """ Wegbot base command error """
    def __init__(self, message=None, *args):
        super().__init__(message, *args)

class RoleNotFoundError(WegbotCommandError):
    """ Role not found """
    def __init__(self, role_name):
        super().__init__(message=f"Role not found: {role_name}")
        self.role_name = role_name

class IneligibleRoleError(WegbotCommandError):
    """ Role cannot be added """
    def __init__(self, role):
        super().__init__(message=f"Role '{role.name}' is ineligible to be added")
        self.role = role
