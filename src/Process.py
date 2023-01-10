from src.Candidate import Candidate


class Process:
    name: str
    cost: tuple[int]
    gain: tuple[int]
    delay: int

    def __init__(self, name: str, cost: tuple[int], gain: tuple[int], delay: int):
        self.name = name
        self.cost = cost
        self.gain = gain
        self.delay = delay

    def __str__(self):
        c: list[str] = []
        g: list[str] = []

        for key, cost, gain in zip(Candidate.converter, self.cost, self.gain):
            if cost:
                c.append(f"{key}:{str(cost)}")
            if gain:
                g.append(f"{key}:{str(gain)}")
        return " - ".join([self.name, f'cost: ({";".join(c)})', f'gain: ({";".join(g)})', str(self.delay)])
