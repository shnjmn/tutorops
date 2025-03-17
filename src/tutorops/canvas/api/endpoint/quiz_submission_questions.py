from ..client import CanvasClient


class QuizSubmissionQuestionsApi:
    def __init__(self, canvas: CanvasClient) -> None:
        self.canvas = canvas

    def index(self, quiz_submission_id, attempt=None):
        """
        Get all quiz submission questions.
        https://canvas.instructure.com/doc/api/quiz_submission_questions.html
        """
        url = f"/api/v1/quiz_submissions/{quiz_submission_id}/questions"
        params = {"quiz_submission_attempt": attempt} if attempt else {}
        return (
            self.canvas.get(url, params=params).json().get("quiz_submission_questions")
        )
