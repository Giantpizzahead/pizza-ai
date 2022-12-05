from pizzaenvs.base import Environment, Action, Agent
from pizzaenvs.calculatorenv import *


def main():
    env = CalculatorEnv()
    action_list = [
        create_action(get_num1, env),
        create_action(get_num2, env),
        create_action(set_answer, env),
    ]
    for i in range(10):
        agent = Agent()
        for action in action_list:
            agent.add_action(action)
        env.add_agent(agent)
    print(env.get_agents()[0].invoke_action("get_num1"))
    print(env.get_agents())
