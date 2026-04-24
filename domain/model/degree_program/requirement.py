from enum import Enum
from domain.model.course import Course

class NodeType(Enum):
    AND = "and"
    OR = "or"
    XOR = "xor"
    COURSE = "course"
    CONSTRAINT = "constraint"

class Requirement:

    @classmethod
    def create_operator(cls, node_type: NodeType, requirements: list["Requirement"]) -> "Requirement":
        return cls(node_type, requirements, None, None)

    @classmethod
    def create_course(cls, course: Course) -> "Requirement":
        return cls(NodeType.COURSE, [], course, None)
    
    @classmethod
    def create_constraint(cls, constraint: dict) -> "Requirement":
        return cls(NodeType.CONSTRAINT, None, None, constraint)

    def __init__(self, node_type: NodeType, requirements: list["Requirement"] | None, course: Course | None, constraint: dict | None):
        self.node_type = node_type
        self.requirements = requirements
        self.course = course
        self.constraint = constraint
