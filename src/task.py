from __future__ import annotations

class Task:
    name: str
    input: dict[str, int]
    output: dict[str, int]
    duration: int

    def __init__(self, name: str, input: dict[str, int], output: dict[str, int], duration: int):
        self.name = name
        self.input = input
        self.output = output
        self.duration = duration

    def __str__(self) -> str:
        return f"{self.name} {self.input} {self.output} {self.duration}"

