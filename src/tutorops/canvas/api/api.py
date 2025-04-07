from .client import CanvasClient
from .endpoint.assignments import AssignmentsApi
from .endpoint.files import FilesApi
from .endpoint.quiz_submission_questions import QuizSubmissionQuestionsApi
from .endpoint.quiz_submissions import QuizSubmissionsApi
from .endpoint.rubrics import RubricsApi
from .endpoint.submissions import SubmissionsApi
from .endpoint.users import UsersApi


class CanvasAPI:
    def __init__(
        self,
        http: CanvasClient | None = None,
        *,
        course_id,
        assignment_id=None,
        quiz_id=None,
    ) -> None:
        self.http = http or CanvasClient()

        self.course_id = course_id
        self.assignment_id = assignment_id
        self.quiz_id = quiz_id

    @property
    def assignments(self):
        if not self.course_id:
            raise ValueError("course_id is required")

        return AssignmentsApi(self.http, self.course_id)

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

    @property
    def users(self):
        return UsersApi(self.http)

    def graphql(self, query, variables=None):
        """
        GraphQL Endpoint
        https://canvas.instructure.com/doc/api/file.graphql.html#graphql-endpoint
        """
        url = "/api/graphql"
        return self.http.post(url, json={"query": query, "variables": variables}).json()

    def list_active_students(self):
        query = """
        query ListActiveStudents($course_id: ID!) {
          course(id: $course_id) {
            usersConnection(
              filter: {enrollmentTypes: StudentEnrollment, enrollmentStates: active}
            ) {
              nodes {
                _id
                name
                sisId
                integrationId
              }
            }
          }
        }
        """
        resp = self.graphql(query, {"course_id": self.course_id})
        return resp["data"]["course"]["usersConnection"]["nodes"]
