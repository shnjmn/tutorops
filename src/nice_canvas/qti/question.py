from typing import Iterable

import pyxb.utils.domutils

from . import binding

pyxb.utils.domutils.BindingDOMSupport.SetDefaultNamespace(binding.Namespace)


class Question:
    title: str
    question_type: str
    points_possible: float
    html: str

    def __init__(self, title: str, html: str, points: float):
        self.title = title
        self.html = html
        self.points_possible = points

    @property
    def qtimetadata(self):
        return binding.qtimetadata(
            binding.qtimetadatafield(
                fieldlabel="question_type",
                fieldentry=self.question_type,
            ),
            binding.qtimetadatafield(
                fieldlabel="points_possible",
                fieldentry=str(self.points_possible),
            ),
        )

    @property
    def mattext_html(self):
        return binding.mattext(self.html, texttype="text/html")

    @property
    def presentation(self):
        return binding.presentation(binding.material(self.mattext_html))

    @property
    def resprocessing(self):
        return None

    @property
    def xml(self):
        root = binding.item(ident=str(id(self)), title=self.title)
        root.append(binding.itemmetadata(self.qtimetadata))
        root.append(self.presentation)

        if self.resprocessing:
            root.append(self.resprocessing)
        return root


class EssayQuestion(Question):
    question_type = "essay_question"

    def __init__(self, title: str, html: str, points: float):
        super().__init__(title, html, points)

    @property
    def response_str(self):
        return binding.response_str(
            ident="response1",
            rcardinality="Single",
            render_fib=binding.render_fib(
                binding.response_labelType(ident="answer1", rshuffle="No")
            ),
        )

    @property
    def presentation(self):
        root = super().presentation
        root.append(self.response_str)
        return root


class FileUploadQuestion(Question):
    question_type = "file_upload_question"

    def __init__(self, title: str, html: str, points: float):
        super().__init__(title, html, points)


class FillInMultipleBlanksQuestion(Question):
    question_type = "fill_in_multiple_blanks_question"

    def __init__(
        self,
        title: str,
        html: str,
        points: float,
        answers: dict[str, set[str]],
    ):
        super().__init__(title, html, points)
        self.answers = answers

    @property
    def presentation(self):
        root = super().presentation

        for i, (ident, answers) in enumerate(self.answers.items()):
            root.append(
                binding.response_lid(
                    binding.material(binding.mattext(ident)),
                    binding.render_choice(
                        *(
                            binding.response_labelType(
                                binding.material(
                                    binding.mattext(ans, texttype="text/plain")
                                ),
                                ident=hex((i << 8) + j),
                            )
                            for j, ans in enumerate(answers)
                        )
                    ),
                    ident="response_{}".format(ident),
                )
            )

        return root


class ShortAnswerQuestion(EssayQuestion):
    question_type = "short_answer_question"

    def __init__(self, title: str, html: str, points: float, answers: set[str]):
        super().__init__(title, html, points)
        self.answers = answers

    @property
    def resprocessing(self):
        return binding.resprocessing(
            binding.outcomes(
                binding.decvar(
                    vartype="Decimal",
                    varname="SCORE",
                    minvalue=0,
                    maxvalue=1,
                )
            ),
            binding.respcondition(
                binding.conditionvar(
                    *(
                        binding.varequal(answer, respident="response1")
                        for answer in self.answers
                    )
                ),
                binding.setvar(
                    1,
                    action="Set",
                    varname="SCORE",
                ),
                continue_="No",
            ),
        )


def create_question_bank(questions: Iterable[Question]):
    root = binding.questestinterop()
    for question in questions:
        root.append(question.xml)
    return root
