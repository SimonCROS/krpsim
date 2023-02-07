class Process:
    id: int
    name: str
    cost: tuple[int]
    gain: tuple[int]
    delay: int

    max_delay: int = 0

    def __init__(self, id: int, name: str, cost: tuple[int], gain: tuple[int], delay: int):
        self.id = id
        self.name = name
        self.cost = cost
        self.gain = gain
        self.delay = delay

        if self.delay > Process.max_delay:
            Process.max_delay = self.delay
