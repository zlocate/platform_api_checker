from pydantic import BaseModel


class CreateStandRequest(BaseModel):
    yuid: str
    stand_number: str
    task_number: str
    def __hash__(self):
        return hash((self.task_number, self.stand_number, self.yuid))
