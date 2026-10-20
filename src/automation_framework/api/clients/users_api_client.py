from playwright.sync_api import APIRequestContext, APIResponse


class UsersApiClient:
    def __init__(self, request_context: APIRequestContext) -> None:
        self.request_context = request_context

    def register(self, payload: dict[str, str]) -> APIResponse:
        return self.request_context.post("/users/register", data=payload)

    def login(self, payload: dict[str, str]) -> APIResponse:
        return self.request_context.post("/users/login", data=payload)

    def get_current_user(self, token: str | None = None) -> APIResponse:
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        return self.request_context.get("/users/me", headers=headers)

    def get_user_by_id(
        self,
        user_id: str,
        token: str | None = None,
    ) -> APIResponse:
        headers: dict[str, str] = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        return self.request_context.get(f"/users/{user_id}", headers=headers)

    def update_user(
        self,
        user_id: str,
        payload: dict[str, object],
        token: str | None = None,
    ) -> APIResponse:
        headers: dict[str, str] = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        return self.request_context.patch(
            f"/users/{user_id}",
            data=payload,
            headers=headers,
        )
