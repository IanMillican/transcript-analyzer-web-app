import os
from exceptions.invalid_argument import InvalidArgumentException
from data_access.parser.degree_parser import parse_degree
from domain.model.degree_program.degree import Degree
from domain.model.degree_program.requirement import Requirement, NodeType

def get_degree(path: str) -> Degree:
    if not os.path.exists(path):
        raise InvalidArgumentException(f"No degree program file found at {path}")
    return parse_degree(path=path)

def pretty_print_degree(degree: Degree) -> str:
    lines = [f"Program: {degree.program}"]
    for section in sorted(degree.sections, key=lambda s: s.priority):
        lines.append(f"\n  Section: {section.name} (priority {section.priority})")
        lines.append(_pretty_print_requirement(section.requirements, indent=4))
    return "\n".join(lines)

def _pretty_print_requirement(req: Requirement, indent: int) -> str:
    prefix = " " * indent
    if req.type == NodeType.COURSE:
        return f"{prefix}- {req.course.course_code}: {req.course.name} ({req.course.credit_hours}ch)"
    else:
        lines = [f"{prefix}[{req.type.value.upper()}]"]
        for child in req.requirements:
            lines.append(_pretty_print_requirement(child, indent + 2))
        return "\n".join(lines)
