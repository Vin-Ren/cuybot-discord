from enum import IntFlag
from discord.ext import commands

from typing import List, Dict, Union

from command_prepared_decorator import Cooldown, Command, DecoratorPriority, HasPerms, BotHasPerms
from command_help import list_help_cmd_hashmap


class ConfigFlags(IntFlag):
    @classmethod
    def all_enabled(cls):
        return cls(sum(list(cls)))
    
    @classmethod
    def all_disabled(cls):
        return ~cls.all_enabled()

    NAME = 1
    ALIASES = 2
    COOLDOWN = 4
    HAS_PERMS = 8
    BOT_HAS_PERMS = 16


class CommandConfig:
    __slots__ = ['name', 'command', 'desc', 'usage', 'aliases', 'additional_decorators']
    
    _DEFAULTS  = {}
    
    def __init__(self, name: str, command: str, desc: str, usage: str, aliases: List[str], 
                 cooldown: Union[Cooldown, int] = None, 
                 has_perms: Union[HasPerms, Dict[str, bool]] = None, 
                 bot_has_perms: Union[BotHasPerms, Dict[str, bool]] = None, 
                 flags: ConfigFlags = ConfigFlags.all_enabled()):
        self.name = name
        self.command = command
        self.desc = desc
        self.usage = usage
        self.aliases = aliases
        self.additional_decorators = {ConfigFlags.COOLDOWN: cooldown if isinstance(cooldown, (Cooldown, None.__class__)) else Cooldown(1, cooldown, commands.BucketType.user), 
                                      ConfigFlags.HAS_PERMS: has_perms if isinstance(has_perms, (HasPerms, None.__class__)) else HasPerms(has_perms), 
                                      ConfigFlags.BOT_HAS_PERMS: bot_has_perms if isinstance(bot_has_perms, (BotHasPerms, None.__class__)) else HasPerms(bot_has_perms)}
        self.flags = flags

    def get_decorator(self):
        def decorate(func):
            # Decorators
            decorators = []
            decorators.append(Command(name=self.name if ConfigFlags.NAME in self.flags else None,
                                      aliases=self.aliases if ConfigFlags.ALIASES in self.flags else None))
            decorators.extend([decorator for flag, decorator in self.additional_decorators.items() if flag in self.flags])
            
            # Checks for LAST and FIRST priority
            decorators_priority_list = [_cls._PRIORITY for _cls in decorators]
            for priority in [DecoratorPriority.LAST, DecoratorPriority.FIRST]:
                if decorators_priority_list.count(priority) > 1:
                    raise RuntimeError("Decorators with priority:{} should only be one.".format(priority.name))
            
            # Post decorators addition, remove None, then sort according to priority, lowest first, highest last.
            decorators = sorted([decor for decor in decorators if decor is not None], key=lambda _cls:_cls._PRIORITY)
            
            for decorator in decorators:
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
