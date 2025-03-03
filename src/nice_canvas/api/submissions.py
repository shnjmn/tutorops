from .http import CanvasClient


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

    def get_single_submission_courses(
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
