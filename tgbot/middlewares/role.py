from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.role import UserRole


class RoleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, admin_ids: list[int]):
        super().__init__()
        self.admin_ids = admin_ids

    async def pre_process(self, obj, data, *args):
        if not getattr(obj, "from_user", None):
            data["role"] = None
        elif obj.from_user.id in self.admin_ids:
            data["role"] = UserRole.ADMIN
        else:
            data["role"] = UserRole.USER

    async def post_process(self, obj, data, *args):
        del data["role"]
