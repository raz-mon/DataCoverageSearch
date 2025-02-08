from typing import List, Optional, Set
from basicDataSet import BasicDataSet
from pattern import Pattern

class DeepDiver:
    def __init__(self, dataset_path: str, threshold: float, interestedIndexes: Optional[List[int]] = None):
        self.dataset = BasicDataSet(dataset_path, interestedIndexes)
        self.threshold = threshold

    def find_max_uncovered_pattern_set(self, threshold) -> List[Pattern]:
        mups: Set[Pattern] = set()
        root = Pattern.get_root_pattern(self.dataset.getDimension())
        stack = [root]

        while stack:
            current_pattern = stack.pop()
            uncovered_flag = False

            if any(mup.is_ancestor_of(current_pattern) for mup in mups):
                continue
            elif any(current_pattern.is_ancestor_of(mup) for mup in mups):
                uncovered_flag = True
            else:
                coverage = self.dataset.checkCoverage(current_pattern)
                uncovered_flag = coverage < threshold

            if uncovered_flag:
                temp_pattern = current_pattern
                temp_stack = [current_pattern]
                while temp_stack:
                    temp_pattern = temp_stack.pop()
                    parent_patterns = temp_pattern.gen_parents()
                    for parent in parent_patterns:
                        parent_coverage = self.dataset.checkCoverage(parent)
                        if parent_coverage < threshold:
                            temp_stack.append(parent)
                            break
                mups.add(temp_pattern)
            else:
                children = current_pattern.gen_children(self.dataset, rule1=True)
                stack.extend(children)

        return list(mups)
