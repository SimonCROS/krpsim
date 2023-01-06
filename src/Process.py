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
        return f"{self.name} - {self.cost} - {self.gain} - {self.delay}"
