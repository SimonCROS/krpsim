class Candidate:
    process: list[int]
    stock: tuple[int]
    fitness: int
    duration: int

    converter: dict[str: int]

    def __init__(self, process: list[int], stock: tuple[int], fitness: int):
        self.process = process
        self.stock = stock
        self.fitness = fitness
        self.duration = 0

    def __str__(self):
        return f"{len(self.process)} - {self.stock} - {self.fitness} - {self.duration}"

    def show_stock(self):
        output: list = []
        for key, stock in zip(Candidate.converter, self.stock):
            output.append(f"{key}: {stock}")
        print(" | ".join(output))
