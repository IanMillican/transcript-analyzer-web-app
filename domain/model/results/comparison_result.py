from domain.model.results.section_result import SectionResult

class ComparisonResult:
    def __init__(self, section_results: list[SectionResult]):
        self.section_results = list(section_results)