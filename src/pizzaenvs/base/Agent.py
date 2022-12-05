from typing import Iterable, Any

from pizzaenvs.base.Action import Action


class Agent:
    """
    A base agent.
    """
    _rolling_id: int = 0
    """The ID assigned to new agents."""

    _id: int
    _actions: dict[str, Action]

    def __init__(self, actions: Iterable[Action] = None) -> None:
        """
        Initializes the agent.

        :param actions: A list of actions that the agent can perform.
        """
        self._id = Agent._rolling_id
        Agent._rolling_id += 1

        self._actions = {}
        if actions is not None:
            for action in actions:
                self.add_action(action)

    @property
    def id(self) -> int:
        """
        Returns the ID of the agent.
        """
        return self._id

    def add_action(self, action: Action) -> None:
        """
        Adds an action to the agent.

        :param action: The action to add.
        :raises AssertionError: If the action already exists.
        """
        assert action.name not in self._actions, f"Action {action.name} already exists"
        self._actions[action.name] = action

    def remove_action(self, action: Action) -> None:
        """
        Removes an action from the agent.

        :param action: The action to remove.
        :raises AssertionError: If the action does not exist.
        """
        assert action.name in self._actions, f"Action {action.name} does not exist"
        del self._actions[action.name]

    def _get_action(self, action_name: str) -> Action:
        """
        Returns the action with the given name.

        :param action_name: The name of the action.
        :return: The action.
        :raises AssertionError: If the action does not exist.
        """
        assert action_name in self._actions, f"Action {action_name} does not exist"
        return self._actions[action_name]

    def invoke_action(self, action_name: str, *args, **kwargs) -> Any:
        """
        Invokes the action with the given name and arguments.

        :param action_name: The action name to invoke.
        :param args: The arguments to pass to the action.
        :param kwargs: The keyword arguments to pass to the action.
        """
        return self._get_action(action_name).invoke(self, *args, **kwargs)

    def step(self) -> None:
        """
        Perform a single step in the environment.
        """
        raise NotImplementedError()

    @staticmethod
    def mutate(agent: "Agent") -> "Agent":
        """
        Returns a mutated version of the agent.

        :param agent: The agent to mutate.
        :return: The mutated agent.
        """
        raise NotImplementedError()

    @staticmethod
    def mate(agent_1: "Agent", agent_2: "Agent") -> "Agent":
        """
        Returns an agent representing the offspring of the two given agents.

        :param agent_1: The first agent.
        :param agent_2: The second agent.
        :return: The offspring.
        """
        raise NotImplementedError()

    def __copy__(self) -> "Agent":
        """
        Returns a copy of the agent (with a different ID!).
        """
        return Agent(actions=self._actions.values())

    def __str__(self) -> str:
        """
        Returns a string representation of the agent.
        """
        return f"Agent with id {self.id}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the agent.
        """
        return f"Agent[id={self.id}]"
