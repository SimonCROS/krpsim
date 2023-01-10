class Candidate:
    process: list[int]
    stock: tuple[int]
    fitness: int
    duration: int

    def __init__(self, process: list[int], stock: tuple[int], fitness: int):
        self.process = process
        self.stock = stock
        self.fitness = fitness
        self.duration = 0

    def __str__(self):
        return f"{len(self.process)} - {self.stock} - {self.fitness} - {self.duration}"
