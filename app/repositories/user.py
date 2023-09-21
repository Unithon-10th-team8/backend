from app import orm


class UserRepository:
    def __init__(self) -> None:
        ...

    async def get(self, user_id: int) -> orm.User:
        ...

    async def get_by_uid(self, uid: int | str) -> orm.User:
        ...

    async def create(self, user: orm.User) -> orm.User:
        ...
