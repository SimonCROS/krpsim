from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Node:
    process: int
    stock: tuple[int]
    delay: int
