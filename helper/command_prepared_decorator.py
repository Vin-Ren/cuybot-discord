from discord.ext import commands

from enum import IntEnum


__all__ = ['Cooldown']


class DecoratorPriority(IntEnum):
    """
    Priority for given Prepared Decorator. Used to determine the order in which, the decorators are applied. 
    The lowest priority is applied first and the highest priority is applied last.
    """
    LOWEST = 0
    LOW = 1
    MEDIUM = NORMAL = 2
    HIGH = 3
    HIGHEST = 4


class BasePreparedDecorator:
    """
    Base class to inherit from for prepared decorators.
    On object initialization, subclasses must call upon super().__init__ method.
    if given _DECORATOR_FUNCTION directly decorate a function, you do not need to pass any kwargs to the super().__init__() function. 
    however if it needs any kwargs, you need to add all of it into the __slots__ class variable and also pass it into the super().__init__() function as kwargs.
    
    to apply a prepared decorator, just use 'example_preped_deco.apply(func)' or directly call __call__ by 'example_preped_deco(func)' where example_preped_deco is the PreparedDecorator object.
    _DECORATOR_FUNCTION is the decorator function which is going to be wrapped.
    
    To update the kwargs to be passed during decorator creation, call the .update() method, this method functions similiarly to dictionary.update() method, pass a dictionary(positional only) to update it, or directly pass kwargs to it, or both. 
    Keep in mind that when passing both, the positional dictionary will be updated by the kwargs given.
    """
    __slots__ = []
    
    _DECORATOR_FUNCTION = None
    _PRIORITY = DecoratorPriority.LOWEST
    
    def __init__(self, __dict={}, /, **kwargs):
        __dict.update(kwargs)
        [setattr(self, k, v) for k,v in __dict.items() if k in self.__class__.__slots__]
    
    def apply(self, func):
        if len(self.__class__.__slots__) > 0:
            decorator = self.__class__._DECORATOR_FUNCTION(**{name:getattr(self, name) for name in self.__class__.__slots__})
        else:
            decorator = self.__class__._DECORATOR_FUNCTION
        return decorator(func)
    
    def __call__(self, func, *, **kwargs):
        self.update(**kwargs)
        return self.apply(func)
    
    def update(self, __dict={}, /, **kwargs):
        __dict.update(kwargs)
        [setattr(self, k, v) for k,v in __dict.items() if k in self.__class__.__slots__]


class Cooldown(BasePreparedDecorator):
    __slots__ = ['rate', 'per', 'type']
    
    _DECORATOR_FUNCTION = commands.Cooldown
    _PRIORITY = DecoratorPriority.LOW
    
    def __init__(self, rate: int, per: int, type: commands.BucketType.default):
        super().__init__(rate=rate, per=per, type=type)

# TODO: Add Prepared decorators for permissions, roles, etc.
