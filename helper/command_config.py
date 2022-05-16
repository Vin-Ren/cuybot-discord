from enum import IntFlag
from discord.ext import commands

from typing import List, Union

from .command_prepared_decorator import Cooldown
from .command_help import list_help_cmd_hashmap


class ConfigFlags(IntFlag):
    @classmethod
    def get_all(cls):
        return cls(sum(list(cls)))
    NAME = 1
    ALIASES = 2
    COOLDOWN = 4
    
    NO_NAME = ~NAME
    NO_ALIASES = ~ALIASES
    NO_COOLDOWN = ~COOLDOWN


class CommandConfig:
    __slots__ = ['name', 'command', 'desc', 'usage', 'aliases', 'cooldown']
    
    _DEFAULTS  = {}
    
    def __init__(self, name: str, command: str, desc: str, usage: str, aliases: List[str], cooldown: Union[Cooldown, int] = None, flags: ConfigFlags = ConfigFlags.get_all()):
        self.name = name
        self.command = command
        self.desc = desc
        self.usage = usage
        self.aliases = aliases
        self.cooldown = cooldown if isinstance(cooldown, (Cooldown, None)) else Cooldown(1, cooldown, commands.BucketType.user)
        self.flags = flags

    def get_decorator(self):
        def decorate(func):
            # Decorators
            decorators = [self.cooldown if ConfigFlags.COOLDOWN in self.flags else None]
            
            # Post decorators addition, remove None, then sort according to priority, lowest first, highest last.
            decorators = sorted([decor for decor in decorators if decor is not None], key=lambda _cls:_cls._PRIORITY)
            
            # Last applied decorators, if the order matters then the list order matters.
            last_applied_decorators = [commands.command(name=self.name if ConfigFlags.NAME in self.flags else None, 
                                                        aliases=self.aliases if ConfigFlags.ALIASES in self.flags else None)]
            
            for decorator in decorators+last_applied_decorators:
                func = decorator(func)
            return func
        return decorate
    
    def __call__(self, function):
        return self.get_decorator()(function)

# TODO: make another class/function (prefferably function) to lookup the values for init for CommandConfig with given 'id' or 'name'
# Then used like @command(name='help'). it will create a CommandConfig object and apply the decorator to the decorated function.

def command(name: str, flags: ConfigFlags = None):
    try:
        def decorator(func):
            kwargs = list_help_cmd_hashmap[name]
            kwargs.update(flags=flags) if flags is not None else None
            return CommandConfig(**kwargs)(func)
        return decorator
    except KeyError:
        raise RuntimeError("Given name={} does not exists in command configuration list.".format(name))
