from domain.model.course_attempt import CourseAttempt
from domain.model.degree_program.requirement import Requirement, NodeType

class RequirementResult:

    @classmethod
    def create_leaf_requirement_result(cls, original_requirement: Requirement, satisfied: bool, course: CourseAttempt | None):
        return cls(original_requirement, satisfied, course, None, None, None)
    
    @classmethod
    def create_operator_result(cls, original_requirement: Requirement, satisfied: bool, child_results: list["RequirementResult"], selected_index: int | None):
        return cls(original_requirement, satisfied, None, None, list(child_results), selected_index)

    @classmethod
    def create_constraint_result(cls, original_requirement: Requirement, satisfied: bool, constraint_matches: dict[int, list[CourseAttempt]]):
        return cls(original_requirement, satisfied, None, constraint_matches, None, None)

    def __init__(self, original_requirement: Requirement, satisfied: bool, course_attempt: CourseAttempt| None, constraint_matches: dict[int: list[CourseAttempt]] | None, child_results: list["RequirementResult"] | None, selected_index: int | None):
        self.original_requirement = original_requirement
        self.satisfied = satisfied
        self.course_attempt = course_attempt
        self.constraint_matches = constraint_matches
        self.child_results = child_results
        self.selected_index = selected_index

    def get_branch_course_status(self) -> list[tuple[str, bool]]:
        if self.original_requirement.node_type == NodeType.COURSE:
            return [(self.original_requirement.course.course_code, self.satisfied)]
        elif self.original_requirement.node_type == NodeType.CONSTRAINT:
            return []
        else:
            statuses = []
            for child in self.child_results:
                statuses.extend(child.get_branch_course_status())
            return statuses