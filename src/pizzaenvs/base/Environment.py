from pizzaenvs.base.Agent import Agent


class Environment:
    """
    A base environment.
    """
    _name: str = "Base Environment"
    _agents: list[Agent]

    def __init__(self) -> None:
        """
        Initializes the environment.
        """
        self._agents = []

    def add_agent(self, agent: Agent) -> None:
        """
        Adds an agent to the environment.
        """
        assert agent not in self._agents, f"Agent {agent.id} already exists"
        agent._environment = self
        self._agents.append(agent)

    def remove_agent(self, agent: Agent) -> None:
        """
        Removes an agent from the environment.
        """
        assert agent in self._agents, f"Agent {agent.id} does not exist"
        agent._environment = None
        self._agents.remove(agent)

    def get_agents(self) -> list[Agent]:
        """
        Returns a list of agents in the environment.
        """
        return self._agents.copy()

    def step(self) -> None:
        """
        Perform a single step in the environment.
        """
        for agent in self.get_agents():
            agent.step()

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
