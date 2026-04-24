from domain.model.course import Course
from domain.model.course_attempt import CourseAttempt
from domain.model.degree_program.requirement import Requirement, NodeType
from domain.model.degree_program.degree import Degree
from domain.model.degree_program.section import Section
from domain.model.results.comparison_result import ComparisonResult
from domain.model.results.section_result import SectionResult
from domain.model.results.requirement_result import RequirementResult
import copy

INVALID_GRADES = [
    "F",
    "W",
    "WF",
    "INC",
    "NCR",
    "N/A",
    ""
]

def _branch_gpa(res: RequirementResult) -> float:
    gp, ch = _branch_gpa_totals(res)
    return gp / ch if ch > 0 else 0.0

def _count_unsatisfied(res: RequirementResult) -> int:
    if res.original_requirement.node_type in (NodeType.COURSE, NodeType.CONSTRAINT):
        return 0 if res.satisfied else 1
    else: 
        return sum(_count_unsatisfied(child) for child in res.child_results)

def _branch_gpa_totals(res: RequirementResult) -> tuple[float, float]:
    if res.original_requirement.node_type == NodeType.COURSE:
        if not res.satisfied:
            return (0.0, 0.0)
        ch = res.course_attempt.credit_hours
        gp = ch * CourseAttempt.GRADE_POINT_MAP.get(res.course_attempt.grade, 0.0)
        return (gp, ch)
    elif res.original_requirement.node_type == NodeType.AND:
        ch = gp = 0
        for r in res.child_results:
            r_gp, r_ch = _branch_gpa_totals(r)
            gp += r_gp
            ch += r_ch
        return (gp, ch)
    elif res.original_requirement.node_type in (NodeType.OR, NodeType.XOR):
        return _branch_gpa_totals(res.child_results[res.selected_index])

def _match_course(req: Requirement, course_pool: list[CourseAttempt]) -> CourseAttempt | None:
    req_course = req.course
    best_course = None
    for ca in course_pool:
        if ca == req_course and ca.grade not in INVALID_GRADES:
            if best_course is None:
                best_course = ca
            elif CourseAttempt.grade_comparator(best_course.grade, ca.grade) > 0:
                best_course = ca
    
    return best_course

def _evaluate_course(req: Requirement, course_pool: list[CourseAttempt]) -> RequirementResult:
    matched_course = _match_course(req=req, course_pool=course_pool)
    if matched_course is None:
        return RequirementResult.create_leaf_requirement_result(req, False, None)
    else:
        course_pool.remove(matched_course)
        return RequirementResult.create_leaf_requirement_result(req, True, matched_course)
    
def _evaluate_and(req: Requirement, course_pool: list[CourseAttempt]) -> RequirementResult:

    satisfied = True
    child_results = []

    for r in req.requirements:
        new_eval = evaluate_requirement(r, course_pool)
        if not new_eval.satisfied:
            satisfied = False
        child_results.append(new_eval)
    
    return RequirementResult.create_operator_result(req, satisfied, child_results, None)

def _evaluate_or(req: Requirement, course_pool: list[CourseAttempt]) -> RequirementResult:
    
    satisfied = False
    child_results = []
    possible_branches = []

    for i, r in enumerate(req.requirements):
        pool_copy = copy.deepcopy(course_pool)
        new_eval = evaluate_requirement(r, pool_copy)
        copies_used = [c for c in course_pool if c not in pool_copy]
        child_results.append(new_eval)
        if new_eval.satisfied:
            possible_branches.append((i, new_eval, copies_used))
    
    if possible_branches:
        satisfied = True
        best = max(possible_branches, key= lambda b: _branch_gpa(b[1]))
        selected_index, _, courses_used = best
        course_pool[:] = [ca for ca in course_pool if ca not in courses_used]
        return RequirementResult.create_operator_result(req, satisfied, child_results, selected_index)
    else:
        best_index = min(range(len(child_results)), key=lambda i: _count_unsatisfied(child_results[i]))
        return RequirementResult.create_operator_result(req, False, child_results, best_index)

def _evaluate_xor(req: Requirement, course_pool: list[CourseAttempt]) -> RequirementResult:

    satisfied = False
    child_results = []
    possible_branches = []

    for i, r in enumerate(req.requirements):
        pool_copy = copy.deepcopy(course_pool)
        new_eval = evaluate_requirement(r, pool_copy)
        copies_used = [c for c in course_pool if c not in pool_copy]
        child_results.append(new_eval)
        if new_eval.satisfied:
            possible_branches.append((i, new_eval, copies_used))
    
    if possible_branches:
        satisfied = True
        best = max(possible_branches, key= lambda b: _branch_gpa(b[1]))
        selected_index, _, courses_used = best
        course_pool[:] = [ca for ca in course_pool if ca not in courses_used]
        for i, _, other_courses_used in possible_branches:
            if i != selected_index:
                course_pool[:] = [ca for ca in course_pool if ca not in other_courses_used]
        return RequirementResult.create_operator_result(req, satisfied, child_results, selected_index)
    else:
        best_index = min(range(len(child_results)), key=lambda i: _count_unsatisfied(child_results[i]))
        return RequirementResult.create_operator_result(req, False, child_results, best_index)

def _evaluate_constraint(req: Requirement, course_pool: list[CourseAttempt]) -> RequirementResult:
    constraint = req.constraint
    count = constraint['count']
    min_credit_hour = constraint['min_credit_hours']
    include_subject = constraint['include_subject']
    exclude_subject = constraint['exclude_subject']
    min_level_2000 = constraint['min_level_2000']
    min_level_3000 = constraint['min_level_3000']
    min_level_4000 = constraint['min_level_4000']
    filtered_courses = list(course_pool)
    if len(include_subject) > 0:
        filtered_courses = [c for c in filtered_courses if c.subject in include_subject]
    if len(exclude_subject) > 0:
        filtered_courses = [c for c in filtered_courses if c.subject not in exclude_subject]
    filtered_courses = [c for c in filtered_courses if not c.coop and c.grade not in INVALID_GRADES]
    filtered_courses = sorted(filtered_courses, key=lambda c: CourseAttempt.GRADE_POINT_MAP.get(c.grade, 0.0))
    curr_count = 0
    curr_credit_hour = 0
    curr_2000_level = 0
    curr_3000_level = 0
    curr_4000_level = 0
    maybes = []
    includes = []
    for course in filtered_courses:
        if course.num >= 4000 and curr_4000_level < min_level_4000:
            curr_4000_level += 1
        elif course.num >= 3000 and curr_3000_level < min_level_3000:
            curr_3000_level += 1
        elif course.num >= 2000 and curr_2000_level < min_level_2000:
            curr_2000_level += 1
        else:
            maybes.append(course)
            continue
        includes.append(course)
        curr_count += 1
        curr_credit_hour += course.credit_hours

    for course in maybes:
        if curr_count >= count:
            break
        includes.append(course)
        curr_credit_hour += course.credit_hours
        curr_count += 1

    course_pool[:] = [c for c in course_pool if c not in includes]
    return RequirementResult.create_constraint_result(req, curr_count >= count, {count: includes})


def evaluate_requirement(req: Requirement, course_pool: list[CourseAttempt]) -> RequirementResult:
    req_type = req.node_type
    if req_type == NodeType.COURSE:
        return _evaluate_course(req, course_pool)
    elif req_type == NodeType.AND:
        return _evaluate_and(req, course_pool)
    elif req_type == NodeType.OR:
        return _evaluate_or(req, course_pool)
    elif req_type == NodeType.XOR:
        return _evaluate_xor(req, course_pool)
    elif req_type == NodeType.CONSTRAINT:
        return _evaluate_constraint(req, course_pool)
    else:
        raise ValueError(f"Unknown node type: {req.node_type}")