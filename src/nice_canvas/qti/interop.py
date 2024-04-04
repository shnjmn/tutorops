from typing import Iterable

from . import binding
from .question import Question


def create_question_bank(questions: Iterable[Question]):
    root = binding.questestinterop()
    for question in questions:
        root.append(question.xml)
    return root
