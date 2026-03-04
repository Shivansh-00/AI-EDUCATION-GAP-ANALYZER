from dataclasses import dataclass


@dataclass
class BKTParams:
    p_init: float = 0.25
    p_learn: float = 0.15
    p_guess: float = 0.2
    p_slip: float = 0.1


class BayesianKnowledgeTracer:
    def __init__(self, params: BKTParams | None = None):
        self.params = params or BKTParams()

    def update(self, p_known: float, correct: bool) -> float:
        g, s = self.params.p_guess, self.params.p_slip
        if correct:
            posterior = (p_known * (1 - s)) / (p_known * (1 - s) + (1 - p_known) * g)
        else:
            posterior = (p_known * s) / (p_known * s + (1 - p_known) * (1 - g))

        learned = posterior + (1 - posterior) * self.params.p_learn
        return max(0.0, min(1.0, learned))

    def trace_sequence(self, correctness_sequence: list[bool]) -> list[float]:
        p = self.params.p_init
        out = []
        for ans in correctness_sequence:
            p = self.update(p, ans)
            out.append(p)
        return out
