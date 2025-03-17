from typing import Iterable
from uuid import uuid1

from . import binding
from .question import Question


def create_question_bank(bank_title, questions: Iterable[Question]):
    bank = binding.objectbank(ident=str(uuid1()))

    bank.append(
        binding.qtimetadata(
            binding.qtimetadatafield(
                fieldlabel="bank_title",
                fieldentry=bank_title,
            ),
        )
    )

    for question in questions:
        bank.append(question.xml)

    return binding.questestinterop(bank)
