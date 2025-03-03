from typing import Any, Dict, Optional

from . import CanvasClient


class RubricsController:
    def __init__(self, canvas: CanvasClient, course_id: int) -> None:
        self.canvas = canvas
        self.course_id = course_id

    def create(
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
        Create a single rubric.
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
