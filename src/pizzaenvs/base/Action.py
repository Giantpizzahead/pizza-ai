from typing import Callable, Any


class Action:
    """
    Represents an action that can be "called" to receive information or perform an action.
    In other words, this class represents a function that an Agent can use.
    """
    _name: str
    _action_func: Callable[..., Any]

    def __init__(self, action_func: Callable, name: str = None):
        """
        Initializes the Action.

        :param action_func: The function to invoke upon calling the given Action.
        :param name: The name of the Action, defaults to the function name.
        """
        self._action_func = action_func
        self._name = name if name is not None else action_func.__name__

    @property
    def name(self) -> str:
        """
        Returns the name of the Action.
        """
        return self._name

    def invoke(self, *args, **kwargs) -> Any:
        """
        Invokes the Action with the given arguments.

        :return: The result.
        """
        return self._action_func(*args, **kwargs)

    def __str__(self) -> str:
        """
        Returns a string representation of the Action.
        """
        return f"Action {self._name}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the Action.
        """
        return f"Action[{self._name}]"
