from .http import CanvasClient
from .rubrics import RubricsApi
from .submissions import SubmissionsApi


class FilesApi:
    def __init__(self, canvas: CanvasClient) -> None:
        self.canvas = canvas

    def show(self, file_id):
        """
        Get file
        https://canvas.instructure.com/doc/api/files.html#method.files.api_show
        """
        url = f"/api/v1/files/{file_id}"
        return self.canvas.get(url).json()


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


class ProfileApi:
    def __init__(self, canvas: CanvasClient) -> None:
        self.canvas = canvas

    def settings(self, user_id):
        """
        Get user profile settings.
        https://canvas.instructure.com/doc/api/users.html#method.profile.settings
        """
        url = f"/api/v1/users/{user_id}/profile"
        return self.canvas.get(url).json()


class Canvas:
    def __init__(
        self, http: CanvasClient, *, course_id, assignment_id=None, quiz_id=None
    ) -> None:
        self.http = http

        self.course_id = course_id
        self.assignment_id = assignment_id
        self.quiz_id = quiz_id

    @property
    def profile(self):
        return ProfileApi(self.http)

    @property
    def files(self):
        return FilesApi(self.http)

    @property
    def quiz_submissions(self):
        if not self.course_id or not self.quiz_id:
            raise ValueError("course_id and quiz_id are required")

        return QuizSubmissionsApi(self.http, self.course_id, self.quiz_id)

    @property
    def quiz_submission_questions(self):
        return QuizSubmissionQuestionsApi(self.http)

    @property
    def rubrics(self):
        return RubricsApi(self.http, self.course_id)

    @property
    def submissions(self):
        if not self.course_id or not self.assignment_id:
            raise ValueError("course_id and assignment_id are required")

        return SubmissionsApi(self.http, self.course_id, self.assignment_id)

    def graphql(self, query, variables=None):
        """
        GraphQL Endpoint
        https://canvas.instructure.com/doc/api/file.graphql.html#graphql-endpoint
        """
        url = "/api/graphql"
        return self.http.post(url, json={"query": query, "variables": variables}).json()
