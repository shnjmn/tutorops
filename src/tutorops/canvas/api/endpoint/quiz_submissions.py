from ..client import CanvasClient


class QuizSubmissionsApi:
    def __init__(self, canvas: CanvasClient, course_id, quiz_id) -> None:
        self.canvas = canvas
        self.course_id = course_id
        self.quiz_id = quiz_id

    def update(self, quiz_submission_id, payload):
        """
        Update student question scores and comments.
        https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.update
        """
        url = f"/api/v1/courses/{self.course_id}/quizzes/{self.quiz_id}/submissions/{quiz_submission_id}"
        return self.canvas.put(url, json={"quiz_submissions": [payload]}).json()
