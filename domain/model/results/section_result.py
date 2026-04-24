from domain.model.degree_program.section import Section
from domain.model.results.requirement_result import RequirementResult

class SectionResult:
    def __init__(self, original_section: Section, root_requirement: RequirementResult):
        self.original_section = original_section
        self.root_requirement = root_requirement