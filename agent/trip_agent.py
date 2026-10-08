from agent.graph import graph
from agent.state import TripState


class TripAgent:

    def run(
            self,
            destination: str,
            days: int,
            travelers: int,
            budget: float,
    ) -> TripState:
        state = TripState(
            destination=destination,
            days=days,
            travelers=travelers,
            budget=budget,
        )

        result = graph.invoke(state)

        return TripState(**result)


trip_agent = TripAgent()
