import argparse
import json
import random
from pathlib import Path
from faker import Faker

fake = Faker()
CONCEPTS = ["Arithmetic", "Algebra", "Functions", "Calculus", "Probability", "Linear Algebra", "Trigonometry"]


def make_student(idx: int):
    student_id = f"student-{idx:04d}"
    base = {
        "student_id": student_id,
        "name": fake.name(),
        "email": fake.email(),
        "quiz_results": [],
        "mastery": {},
    }

    for q in range(random.randint(8, 20)):
        concept = random.choice(CONCEPTS)
        correct = random.random() > 0.35
        base["quiz_results"].append({
            "quiz_id": f"quiz-{q:03d}",
            "concept": concept,
            "score": random.randint(40, 100),
            "response_time_ms": random.randint(1200, 12000),
            "correct": correct,
        })

    for c in CONCEPTS:
        base["mastery"][c] = round(random.uniform(0.2, 0.95), 2)
    return base


def main(count: int, output: str):
    data = [make_student(i) for i in range(1, count + 1)]
    Path(output).write_text(json.dumps(data, indent=2))
    print(f"Generated {count} student records at {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=500)
    parser.add_argument("--output", default="backend/scripts/demo_students.json")
    args = parser.parse_args()
    main(args.count, args.output)
