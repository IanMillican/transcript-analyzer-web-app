from dataclasses import dataclass

#Frozen = True makes the class immutable
@dataclass(frozen=True)
class MonthDay:
    month: int
    day: int