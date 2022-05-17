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


class DecoratorEntry:
    def __init__(self, flag: ConfigFlags, decorator_class: type, keyword: str = None, initializer: callable = None):
        self.flag = flag
        self.decorator_class = decorator_class
        self.keyword = keyword if keyword is not None else flag.name.lower()
        self.initializer = initializer if initializer is not None else decorator_class


class CommandConfig:
    __slots__ = ['name', 'command', 'desc', 'usage', 'aliases', 'additional_decorators', 'flags']
    
    _DEFAULTS  = {}
    
    _DECORATORS = [DecoratorEntry(ConfigFlags.COOLDOWN, Cooldown, initializer=lambda cd: Cooldown(1, cd, commands.BucketType.user)),
                   DecoratorEntry(ConfigFlags.HAS_PERMS, HasPerms),
                   DecoratorEntry(ConfigFlags.BOT_HAS_PERMS, BotHasPerms)
                   ]
    
    def __init__(self, name: str, command: str = '', desc: str = '',  usage: str = '', aliases: List[str] = [], 
                 flags: ConfigFlags = ConfigFlags.all_enabled(),
                 **kwargs):
        self.name = name
        self.command = command
        self.desc = desc
        self.usage = usage
        self.aliases = aliases
        
        self.additional_decorators = {e.flag: kwargs.get(e.keyword) if isinstance(kwargs.get(e.keyword), (e.decorator_class, None.__class__)) else e.initializer(kwargs.get(e.keyword)) for e in self.__class__._DECORATORS}
        
        self.flags = flags

    def get_decorator(self):
        def decorate(func):
            # Decorators
            decorators = []
            decorators.append(Command(name=self.name if ConfigFlags.NAME in self.flags else None,
                                      aliases=self.aliases if ConfigFlags.ALIASES in self.flags else None,
                                      description=self.desc, usage=self.usage))
            decorators.extend([decorator for flag, decorator in self.additional_decorators.items() if flag in self.flags])
            
            # Checks for LAST and FIRST priority
            decorators_priority_list = [_cls._PRIORITY for _cls in decorators if _cls is not None]
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


def command(name: str, flags: ConfigFlags = None):
    if list_help_cmd_hashmap.get(name, None) is None:
        raise RuntimeError("Given name={} does not exists in command configuration list.".format(name))
    def decorator(func):
        kwargs = list_help_cmd_hashmap[name]
        kwargs.update(flags=flags) if flags is not None else None
        return CommandConfig(**kwargs)(func)
    return decorator
