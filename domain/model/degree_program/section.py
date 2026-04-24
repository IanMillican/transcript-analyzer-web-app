from domain.model.degree_program.requirement import Requirement

class Section:
    def __init__(self, requirement: Requirement, name: str, priority: int):
        self.requirement = requirement
        self.name = name
        self.priority = priority