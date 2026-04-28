import json
from domain.model.degree_program.degree import Degree
from domain.model.degree_program.section import Section
from domain.model.degree_program.requirement import Requirement, NodeType
from domain.model.course import Course


def parse_degree(path: str) -> Degree:
    with open(path, "r") as f:
        program_dict = json.load(f)
    
    program = program_dict.get("program")
    sections = program_dict.get("sections")
    parsed_sections = _parse_sections(sections=sections)
    excluded_subjects = program_dict.get("excluded_subjects", [])
    excluded_courses = program_dict.get("excluded_courses", [])
    pw_reqs = program_dict.get("pw_requirements", {"min_p_ch": 0, "min_p_courses": 0, "min_w_ch": 0, "min_w_courses": 0})
    degree = Degree(sections=parsed_sections, program=program, excluded_subjects=excluded_subjects, excluded_courses=excluded_courses, pw_requirements=pw_reqs)
    return degree

def _parse_sections(sections: list[dict]) -> list[Section]:
    parsed_sections = []

    for sec in sections:
        name = sec.get("name")
        priority = sec.get("priority")
        reqs = sec.get("requirements")
        parsed_reqs = _parse_requirement(reqs)
        new_sec = Section(requirement=parsed_reqs, name=name, priority=priority)
        parsed_sections.append(new_sec)
    
    return parsed_sections

def _parse_constraint(constraint: dict) -> Requirement:
    return Requirement.create_constraint(constraint=constraint)

def _parse_requirement(reqs: dict) -> Requirement:
    key, val = next(iter(reqs.items()))
    node_type = NodeType(key)
    if node_type == NodeType.CONSTRAINT:
        return _parse_constraint(val)
    sub_reqs = []
    for item in val:
        if "Subject" in item:
            sub_reqs.append(_parse_course(item))
        else:
            sub_reqs.append(_parse_requirement(item))
    
    return Requirement.create_operator(node_type, sub_reqs)

def _parse_course(course: dict) -> Requirement:
    new_course = Course(
        subject=course.get("Subject"),
        num=course.get("Number"),
        name=course.get("Name"),
        credit_hours=course.get("CreditHours"),
        coop=course.get("Coop")
    )
    return Requirement.create_course(new_course)
