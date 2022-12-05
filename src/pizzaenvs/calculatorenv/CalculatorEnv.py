import random

from pizzaenvs.base import Environment


class CalculatorEnv(Environment):
    """
    A calculator environment.
    """

    def __init__(self) -> None:
        """
        Initializes the environment.
        """
        super().__init__()
        self._name = "Calculator Environment"
        self.num1: int = 0
        self.num2: int = 0
        self.answers: dict[int, int] = {}

    @property
    def num3(self) -> int:
        """
        Returns the sum of num1 and num2.
        """
        return self.num1 + self.num2

    def step(self) -> None:
        """
        Perform a single step in the environment.
        """
        super().step()
        self.num1 = random.randint(0, 1)
        self.num2 = random.randint(0, 1)

    def __str__(self) -> str:
        """
        Returns a string representation of the environment.
        """
        return f"{self._name} with {len(self._agents)} agents"

    def __repr__(self) -> str:
        """
        Returns a string representation of the environment.
        """
        return f"Environment[{self._name}]"
