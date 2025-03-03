from typing import Any, Dict, Optional

from .http import CanvasClient


class RubricsApi:
    def __init__(self, canvas: CanvasClient, course_id: int) -> None:
        self.canvas = canvas
        self.course_id = course_id

    def create_single_rubric(
        self,
        *,
        id: Optional[int] = None,
        rubric_association_id: Optional[int] = None,
        title: Optional[str] = None,
        free_form_criterion_comments: Optional[bool] = None,
        skip_updating_points_possible: Optional[bool] = None,
        criteria: Optional[Dict[str, Any]] = None,
        association_id: Optional[int] = None,
        association_type: Optional[str] = None,
        use_for_grading: Optional[bool] = None,
        hide_score_total: Optional[bool] = None,
        purpose: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics.create
        """
        url = f"/api/v1/courses/{self.course_id}/rubrics"

        assert association_type in (None, "Assignment", "Course", "Account")
        assert purpose in (None, "grading", "bookmark")

        payload = {
            "id": id,
            "rubric_association_id": rubric_association_id,
            "rubric": {
                k: v
                for k, v in {
                    "title": title,
                    "free_form_criterion_comments": free_form_criterion_comments,
                    "skip_updating_points_possible": skip_updating_points_possible,
                    "criteria": criteria,
                }.items()
                if v is not None
            },
            "rubric_association": {
                k: v
                for k, v in {
                    "association_id": association_id,
                    "association_type": association_type,
                    "use_for_grading": use_for_grading,
                    "hide_score_total": hide_score_total,
                    "purpose": purpose,
                }.items()
                if v is not None
            },
        }

        payload = {k: v for k, v in payload.items() if v}
        return self.canvas.post(url, json=payload).json()

    def list_rubrics_courses(self) -> Dict[str, Any]:
        """
        https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index
        """
        url = f"/api/v1/courses/{self.course_id}/rubrics"
        return self.canvas.paginated(url)

    def get_single_rubric_courses(
        self,
        rubric_id: int,
        *,
        assessments=False,
        graded_assessments=False,
        peer_assessments=False,
        associations=False,
        assignment_associations=False,
        course_associations=False,
        account_associations=False,
        style: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show
        """
        url = f"/api/v1/courses/{self.course_id}/rubrics/{rubric_id}"

        params = {}

        include = [
            k
            for k in [
                assessments and "assessments",
                graded_assessments and "graded_assessments",
                peer_assessments and "peer_assessments",
                associations and "associations",
                assignment_associations and "assignment_associations",
                course_associations and "course_associations",
                account_associations and "account_associations",
            ]
            if k
        ]

        assert style in (None, "full", "comments_only")

        if include:
            params["include"] = include

        if style:
            params["style"] = style

        return self.canvas.get(url, params=params).json()

    def create_single_rubric_assessment(
        self,
        rubric_association_id: int,
        user_id: int,
        assessment_type: str,
        assessment: Dict[str, Dict[str, Any]],
    ):
        """
        https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.create
        """
        url = f"/api/v1/courses/{self.course_id}/rubric_associations/{rubric_association_id}/rubric_assessments"

        assert assessment_type in ("grading", "peer_review", "provisional_grade")

        payload = {
            "graded_anonymously": False,
            "rubric_assessment": {
                "user_id": str(user_id),
                "assessment_type": assessment_type,
                **assessment,
            },
        }

        return self.canvas.post(url, json=payload).json()

    def update_single_rubric_assessment(
        self,
        rubric_association_id: int,
        rubric_assessment_id: int,
        user_id: int,
        assessment_type: str,
        assessment: Dict[str, Dict[str, Any]],
    ):
        """
        https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_assessments.update
        """
        url = f"/api/v1/courses/{self.course_id}/rubric_associations/{rubric_association_id}/rubric_assessments/{rubric_assessment_id}"

        assert assessment_type in ("grading", "peer_review", "provisional_grade")

        payload = {
            "rubric_assessment": {
                "user_id": str(user_id),
                "assessment_type": assessment_type,
                **assessment,
            }
        }

        return self.canvas.put(url, json=payload).json()
