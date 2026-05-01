import json
from operator import attrgetter
from domain.service.evaluator import evaluate_requirement
from domain.model.transcript import Transcript
from domain.model.course_attempt import CourseAttempt
from domain.model.degree_program.section import Section
from domain.model.degree_program.degree import Degree
from domain.model.degree_program.requirement import NodeType
from domain.model.results.pw_result import PWResult
from domain.model.results.comparison_result import ComparisonResult
from domain.model.results.section_result import SectionResult
from domain.model.results.requirement_result import RequirementResult
from domain.model.course import Course


def _evaluate_section(section: Section, course_pool: list[CourseAttempt]) -> SectionResult:
    res = evaluate_requirement(section.requirement, course_pool)
    return SectionResult(section, res)

def _get_elective_courses_from_node(req_result: RequirementResult) -> list[Course]:
    result = []
    if req_result.original_requirement.node_type == NodeType.CONSTRAINT:
        return []
    elif req_result.original_requirement.node_type == NodeType.COURSE:
        return [req_result.original_requirement.course]
    else:
        return _get_elective_courses_from_node(req_result.child_results[req_result.selected_index])
    

def _get_elective_courses(section_results: list[SectionResult]) -> list[Course]:
    courses = []
    for sec in section_results: 
        if "elective" in sec.original_section.name.lower():
            courses.extend(_get_elective_courses_from_node(sec.root_requirement))

def get_elective_courses(section_results: list[SectionResult]) -> list[Course]:
    courses = []
    for sec in section_results: 
        if "elective" in sec.original_section.name.lower():
            courses.extend(_get_elective_courses_from_node(sec.root_requirement))
    return courses

def _evaluate_pw() -> PWResult:
    with open("data_access/config/catalogues/pw-courses.json") as f:
        data = json.load(f)
        p_courses = data['PCourses']
        w_courses = data['WCourses']
    # Placeholder values, replace with actual logic to determine these
    min_p_ch = 30
    min_p_courses = 10
    min_w_ch = 15
    min_w_courses = 5
    satisfied_p = []  # List of CourseAttempt that satisfy P requirements
    satisfied_w = []  # List of CourseAttempt that satisfy W requirements

    return PWResult(min_p_ch, min_p_courses, min_w_ch, min_w_courses, satisfied_p, satisfied_w)

def evaluate_transcript(transcript: Transcript, deg_prg: Degree) -> ComparisonResult:

    course_pool = [c for c in transcript.get_courses(degree=deg_prg.program) 
               if c.credit_hours > 0
               and c.subject not in deg_prg.excluded_subjects
               and c.course_code not in deg_prg.excluded_courses]

    sections = sorted(deg_prg.sections, key=attrgetter('priority'))
    section_results = []
    for sec in sections:
        section_results.append(_evaluate_section(sec, course_pool))

    pw_result = _evaluate_pw()
    return ComparisonResult(section_results, pw_result)
