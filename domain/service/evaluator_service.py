from operator import attrgetter
from domain.service.evaluator import evaluate_requirement
from domain.model.transcript import Transcript
from domain.model.course_attempt import CourseAttempt
from domain.model.degree_program.section import Section
from domain.model.degree_program.degree import Degree
from domain.model.results.comparison_result import ComparisonResult
from domain.model.results.section_result import SectionResult


def _evaluate_section(section: Section, course_pool: list[CourseAttempt]) -> SectionResult:
    res = evaluate_requirement(section.requirement, course_pool)
    return SectionResult(section, res)

def evaluate_transcript(transcript: Transcript, deg_prg: Degree) -> ComparisonResult:
    course_pool = [c for c in transcript.get_courses(degree=deg_prg.program) 
               if c.credit_hours > 0
               and c.subject not in deg_prg.excluded_subjects
               and c.course_code not in deg_prg.excluded_courses]
    sections = sorted(deg_prg.sections, key=attrgetter('priority'))
    section_results = []
    for sec in sections:
        section_results.append(_evaluate_section(sec, course_pool))
    
    return ComparisonResult(section_results)
