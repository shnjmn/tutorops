from .interop import create_question_bank
from .question import (
    EssayQuestion,
    FileUploadQuestion,
    FillInMultipleBlanksQuestion,
    ShortAnswerQuestion,
)

__all__ = [
    "create_question_bank",
    "EssayQuestion",
    "FileUploadQuestion",
    "FillInMultipleBlanksQuestion",
    "ShortAnswerQuestion",
    "Nice",
]


class Nice:
    @staticmethod
    def str(ans: set[str]):
        ret = set()
        for a in ans:
            ret.add(a.upper())
            ret.add(a.lower())
        return ret
