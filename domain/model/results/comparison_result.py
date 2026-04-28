from domain.model.results.section_result import SectionResult
from domain.model.results.pw_result import PWResult

class ComparisonResult:
    def __init__(self, section_results: list[SectionResult], pw_result: PWResult | None = None):
        self.section_results = list(section_results)
        self.pw_result = pw_result