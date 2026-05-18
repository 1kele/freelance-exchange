from src.models.responses import ResponsesOrm
from src.repositories.base import BaseRepositories
from src.schemas.response import Response

class ResponseRepository(BaseRepositories):
    model = ResponsesOrm
    schema = Response