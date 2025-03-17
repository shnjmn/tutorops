from ..http import CanvasClient


class UsersApi:
    def __init__(self, canvas: CanvasClient) -> None:
        self.canvas = canvas

    def get_user_profile(self, user_id):
        """
        Get user profile settings.
        https://canvas.instructure.com/doc/api/users.html#method.profile.settings
        """
        url = f"/api/v1/users/{user_id}/profile"
        return self.canvas.get(url).json()
