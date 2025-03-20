import httpx


class GitHub:
    def __init__(self, token: str):
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

    def list_accepted_assignments(self, assignment_id: int, per_page: int = 100):
        resp = self.http.get(
            f"/assignments/{assignment_id}/accepted_assignments",
            params={"per_page": per_page},
        )
        resp.raise_for_status()
        return resp.json()

    def get_latest_release(self, owner: str, repo: str):
        resp = self.http.get(f"/repos/{owner}/{repo}/releases/latest")
        resp.raise_for_status()
        return resp.json()

    def create_release(self, owner: str, repo: str, tag_name: str, name: str):
        resp = self.http.post(
            f"/repos/{owner}/{repo}/releases",
            json={"tag_name": tag_name, "name": name},
        )
        resp.raise_for_status()
        return resp.json()
