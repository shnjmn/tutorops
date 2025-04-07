from ..client import CanvasClient


class AssignmentsApi:
    def __init__(self, canvas: CanvasClient, course_id) -> None:
        self.canvas = canvas
        self.course_id = course_id

    def get_single_assignment(self, assignment_id):
        """
        Get a single assignment by ID.
        """
        url = f"/api/v1/courses/{self.course_id}/assignments/{assignment_id}"
        return self.canvas.get(url).json()
