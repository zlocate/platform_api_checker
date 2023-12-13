from gitlab import Gitlab

from app.models.create_stand_request import CreateStandRequest
from config import Config

gitlab_url = Config.gitlab_url()
private_token = Config.gitlab_private_token()
project_id = Config.gitlab_project_id()
ref = Config.gitlab_branch()


class GitlabClient():

    def __init__(self):
        self.gl = Gitlab(gitlab_url, private_token=private_token)
        self.project = self.gl.projects.get(project_id)

    def run_create_stand_pipeline(self, request: CreateStandRequest) -> int:
        pipeline_parameters = [
            {'key': 'TASK_NUMBER', 'value': request.task_number},
            {'key': 'STAND_NUMBER', 'value': request.stand_number},
            {'key': 'Y_UID', 'value': request.yuid},
        ]

        pipeline = self.project.pipelines.create({'ref': ref, 'variables': pipeline_parameters})

        return pipeline.id

    def check_pipeline_status(self, pipeline_id) -> str:
        pipeline = self.project.pipelines.get(pipeline_id)
        pipeline_status = pipeline.status

        return pipeline_status
