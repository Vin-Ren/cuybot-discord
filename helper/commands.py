from enum import IntFlag
from discord.ext import commands

from typing import List, Dict, Union

from helper.prepared_decorator import Cooldown, Command, DecoratorPriority, HasPerms, BotHasPerms
from helper.commands_config import commands_config


class ConfigFlag(IntFlag):
    @classmethod
    def all_enabled(cls):
        return cls(sum(list(cls)))
    
    @classmethod
    def all_disabled(cls):
        return cls.NULL

    NULL = DISABLED = 0
    
    NAME = 1
    ALIASES = 2
    COOLDOWN = 4
    HAS_PERMS = 8
    BOT_HAS_PERMS = 16



class DecoratorEntry:
    def __init__(self, flag: ConfigFlag, decorator_class: type, keyword: str = None, initializer: callable = None):
        self.flag = flag
        self.decorator_class = decorator_class
        self.keyword = keyword if keyword is not None else flag.name.lower()
        self.initializer = initializer if initializer is not None else decorator_class


class CommandConfig:
    __slots__ = ['name', 'command', 'desc', 'usage', 'aliases', 'additional_decorators', 'flags']
    
    _DEFAULTS  = {}
    
    _DECORATORS = [DecoratorEntry(ConfigFlag.COOLDOWN, Cooldown, initializer=lambda cd: Cooldown(1, cd, commands.BucketType.user)),
                   DecoratorEntry(ConfigFlag.HAS_PERMS, HasPerms),
                   DecoratorEntry(ConfigFlag.BOT_HAS_PERMS, BotHasPerms)
                   ]
    
    def __init__(self, name: str, command: str = '', desc: str = '',  usage: str = '', aliases: List[str] = [], 
                 flags: ConfigFlag = ConfigFlag.all_enabled(),
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
            decorators.append(Command(name=self.name if ConfigFlag.NAME in self.flags else None,
                                      aliases=self.aliases if ConfigFlag.ALIASES in self.flags else [],
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


def command(name: str, flags: ConfigFlag = None, inverse_flags: bool = False, **updater_kwargs):
    """A decorator that wraps :class:`CommandConfig` with command configurations from commands_config.
    
    Parameters
    ----------
    name :class:`str`
        Name of the command, used to search for kwargs from commands_config.
    flags :class:`ConfigFlag`
        Flags to be passed to CommandConfig. Flags are used to modify the behaviour of CommandConfig decorators.
    inverse_flags :class:`bool`
        Inverse given flags by applying a NOT unary operator on the flags.
    """
    flags = ~flags if inverse_flags else flags
    if commands_config.get(name, None) is None:
        raise RuntimeError("Given name='{}' does not exists in command configuration list.".format(name))
    def decorator(func):
        kwargs = commands_config[name]
        kwargs.update(updater_kwargs)
        kwargs.update(flags=flags) if flags is not None else None
        return CommandConfig(**kwargs)(func)
    return decorator
