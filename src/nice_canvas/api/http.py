import os
import re

import httpx


class CanvasClient:
    def __init__(
        self,
        base_url=os.getenv("CANVAS_BASE_URL"),
        token=os.getenv("CANVAS_TOKEN"),
    ):
        if not base_url:
            raise ValueError("CANVAS_BASE_URL is required")

        if not token:
            raise ValueError("CANVAS_TOKEN is required")

        self._http = httpx.Client(
            base_url=base_url,
            follow_redirects=True,
            headers={
                "Authorization": "Bearer {}".format(token),
                "Content-Type": "application/json",
            },
        )

    def get(self, url, *, params=None) -> httpx.Response:
        resp = self._http.request("GET", url, params=params)
        resp.raise_for_status()
        return resp

    def paginated(self, url, *, key=None, params=None, per_page=10):
        reg = re.compile(r'<(?P<url>http\S+)>; rel="(?P<rel>\S+)"')

        if not params:
            params = {}

        params["per_page"] = per_page

        while url:
            resp = self.get(url, params=params)

            data = resp.json()[key] if key else resp.json()
            for item in data:
                yield item

            link = {
                k: v
                for v, k in (
                    reg.match(l).groups() for l in resp.headers.get("link").split(",")
                )
            }
            url = None if link["last"] == link["current"] else link["next"]

    def post(self, url, *, data=None, json=None, params=None):
        resp = self._http.request("POST", url, data=data, json=json, params=params)
        resp.raise_for_status()
        return resp

    def put(self, url, *, data=None, json=None, params=None):
        resp = self._http.request("PUT", url, data=data, json=json, params=params)
        resp.raise_for_status()
        return resp

    def delete(self, url, *, params=None):
        resp = self._http.request("DELETE", url, params=params)
        resp.raise_for_status()
        return resp


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


class SubmissionsApi:
    def __init__(self, canvas: CanvasClient, course_id, assignment_id) -> None:
        self.canvas = canvas
        self.course_id = course_id
        self.assignment_id = assignment_id

    def index(
        self,
        per_page=100,
        *,
        submission_history=True,
        submission_comments=False,
        rubric_assessment=False,
        assignment=False,
        visibility=False,
        course=False,
        user=False,
        group=False,
        read_status=False,
    ):
        """
        List assignment submissions
        https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index
        """
        url = f"/api/v1/courses/{self.course_id}/assignments/{self.assignment_id}/submissions"
        include = [
            k
            for k in [
                submission_history and "submission_history",
                submission_comments and "submission_comments",
                rubric_assessment and "rubric_assessment",
                assignment and "assignment",
                visibility and "visibility",
                course and "course",
                user and "user",
                group and "group",
                read_status and "read_status",
            ]
            if k
        ]
        return self.canvas.paginated(
            url,
            params={"include[]": include},
            per_page=per_page,
        )

    def show(
        self,
        user_id,
        *,
        submission_history=False,
        submission_comments=False,
        rubric_assessment=False,
        full_rubric_assessment=False,
        visibility=False,
        course=False,
        user=False,
        read_status=False,
    ):
        """
        Get a single submission.
        https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show
        """
        url = f"/api/v1/courses/{self.course_id}/assignments/{self.assignment_id}/submissions/{user_id}"
        include = [
            k
            for k in [
                submission_history and "submission_history",
                submission_comments and "submission_comments",
                rubric_assessment and "rubric_assessment",
                full_rubric_assessment and "full_rubric_assessment",
                visibility and "visibility",
                course and "course",
                user and "user",
                read_status and "read_status",
            ]
            if k
        ]
        return self.canvas.get(url, params={"include[]": include}).json()

    def update(self, user_id, payload):
        """
        Grade or comment on a submission.
        https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update
        """
        url = f"/api/v1/courses/{self.course_id}/assignments/{self.assignment_id}/submissions/{user_id}"
        return self.canvas.put(url, json=payload).json()


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
