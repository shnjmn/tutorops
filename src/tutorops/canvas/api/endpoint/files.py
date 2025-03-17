from ..client import CanvasClient


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
