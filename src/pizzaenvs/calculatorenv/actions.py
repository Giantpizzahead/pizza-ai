from typing import Callable

from .CalculatorEnv import CalculatorEnv
from pizzaenvs.base import Agent, Action


def get_num1(env: CalculatorEnv, agent: Agent) -> int:
    return env.num1


def get_num2(env: CalculatorEnv, agent: Agent) -> int:
    return env.num2


def set_answer(env: CalculatorEnv, agent: Agent, answer: int) -> None:
    env.answers[agent.id] = answer


def create_action(func: Callable, env: CalculatorEnv) -> Action:
    def action_func(*args, **kwargs):
        return func(env, *args, **kwargs)
    return Action(action_func, f"{func.__name__}")
