import os

import httpx


class GitHub:
    def __init__(self, token: str = None):
        if not token:
            token = os.getenv("GITHUB_PAT")

        if not token:
            raise ValueError("GitHub token is required")

        self.http = httpx.Client(
            base_url="https://api.github.com",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=300,
            follow_redirects=True,
        )

    def patch(self, url: str, **kwargs):
        resp = self.http.patch(url, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def get(self, url: str):
        resp = self.http.get(url)
        resp.raise_for_status()
        return resp.json()

    def list_commits(self, full_name: str):
        """
        https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#list-commits
        """
        resp = self.http.get(f"/repos/{full_name}/commits")
        resp.raise_for_status()
        return resp.json()

    def list_accepted_assignments(self, assignment_id: int, per_page: int = 100):
        """
        https://docs.github.com/en/rest/classroom/classroom?apiVersion=2022-11-28#list-accepted-assignments-for-an-assignment
        """
        resp = self.http.get(
            f"/assignments/{assignment_id}/accepted_assignments",
            params={"per_page": per_page},
        )
        resp.raise_for_status()
        return resp.json()

    def get_latest_release(self, full_name: str):
        resp = self.http.get(f"/repos/{full_name}/releases/latest")
        resp.raise_for_status()
        return resp.json()

    def create_release(
        self, full_name: str, tag_name: str, name: str, *, target_commitish=None
    ):
        payload = {"tag_name": tag_name, "name": name}
        if target_commitish:
            payload["target_commitish"] = target_commitish

        resp = self.http.post(f"/repos/{full_name}/releases", json=payload)
        resp.raise_for_status()
        return resp.json()
