from pydantic import RootModel


class RegistrationErrorResponse(RootModel[dict[str, list[str]]]):
    pass
