from discord.ext import commands

from typing import List
from enum import IntEnum


__all__ = ['Cooldown']


class DecoratorPriority(IntEnum):
    """
    Priority for given Prepared Decorator. Used to determine the order in which, the decorators are applied. 
    The lowest priority is applied first and the highest priority is applied last. 
    However for FIRST and LAST flags, they are the only outliers, only one of each is allowed in a CommandConfig.
    """
    FIRST = -1
    LOWEST = 0
    LOW = 1
    MEDIUM = NORMAL = 2
    HIGH = 3
    HIGHEST = 4
    LAST = 8


class BasePreparedDecorator:
    """
    Base class to inherit from for prepared decorators.
    On object initialization, subclasses must call upon super().__init__ method.
    if given _DECORATOR_FUNCTION directly decorate a function, you do not need to pass any kwargs to the super().__init__() function. 
    however if it needs any kwargs, you need to add all of it into the __slots__ class variable and also pass it into the super().__init__() function as kwargs.
    
    If you do not want to use slots, you can opt out of it, by setting _USE_SLOTS = False and __slots__ = ['__dict__'] or __slots__ = BasePreparedDecorator._OPT_OUT_SLOTS for the shorthand. This can be useful for example when there's too many kwargs to manage.
    
    You could also leave all the method as it is if you do not want to provide argument hints or there's too many kwargs.
    
    to apply a prepared decorator, just use 'example_preped_deco.apply(func)' or directly call __call__ by 'example_preped_deco(func)' where example_preped_deco is the PreparedDecorator object.
    _DECORATOR_FUNCTION is the decorator function which is going to be wrapped.
    
    To update the kwargs to be passed during decorator creation, call the .update() method, this method functions similiarly to dictionary.update() method, pass a dictionary(positional only) to update it, or directly pass kwargs to it, or both. 
    Keep in mind that when passing both, the positional dictionary will be updated by the kwargs given.
    """
    __slots__ = []
    _OPT_OUT_SLOTS = ['__dict__']
    _USE_SLOTS = True
    _DECORATOR_FUNCTION = None
    _PRIORITY = DecoratorPriority.LOWEST
    
    def __init__(self, __dict={}, /, **kwargs):
        __dict.update(kwargs)
        possible_attrs = self.__class__.__slots__ if self.__class__._USE_SLOTS else [k for k in __dict]
        [setattr(self, k, v) for k,v in __dict.items() if k in possible_attrs]
    
    def apply(self, func):
        possible_attrs = self.__class__.__slots__ if self.__class__._USE_SLOTS else [k for k in self.__dict__]
        if len(self.__class__.__slots__) > 0:
            decorator = self.__class__._DECORATOR_FUNCTION(**{name:getattr(self, name) for name in possible_attrs})
        else:
            decorator = self.__class__._DECORATOR_FUNCTION
        return decorator(func)
    
    def __call__(self, func, /, *_, **kwargs):
        self.update(**kwargs)
        return self.apply(func)
    
    def update(self, __dict={}, /, **kwargs):
        __dict.update(kwargs)
        [setattr(self, k, v) for k,v in __dict.items() if k in self.__class__.__slots__]


class BasePreparedDecoratorNoSlots(BasePreparedDecorator):
    __slots__ = ['__dict__']
    _USE_SLOTS = False


class Command(BasePreparedDecorator):
    __slots__ = ['name', 'aliases', 'brief', 'usage', 'description']
    
    _DECORATOR_FUNCTION = commands.command
    _PRIORITY = DecoratorPriority.LAST
    
    def __init__(self, name: str, aliases: List[str] = [], brief: str = '', usage: str = '', description: str = ''):
        super().__init__(name=name, aliases=aliases, brief=brief, usage=usage, description=description)


class Cooldown(BasePreparedDecorator):
    __slots__ = ['rate', 'per', 'type']
    
    _DECORATOR_FUNCTION = commands.cooldown
    _PRIORITY = DecoratorPriority.LOW
    
    def __init__(self, rate: int, per: int, type: commands.BucketType.default):
        super().__init__(rate=rate, per=per, type=type)


# TODO: Add Prepared decorators for permissions, roles, etc.
class HasPerms(BasePreparedDecoratorNoSlots):
    _DECORATOR_FUNCTION = commands.has_permissions
    _PRIORITY = DecoratorPriority.LOW
    
    def __init__(self, __perms_dict={}, /, **perms):
        __perms_dict.update(perms)
        super().__init__(__perms_dict)


class BotHasPerms(HasPerms):
    _DECORATOR_FUNCTION = commands.bot_has_permissions
