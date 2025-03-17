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
