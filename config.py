import os



class Config:
    @staticmethod
    def gitlab_private_token():
        return os.getenv('GITLAB_TOKEN')

    @staticmethod
    def gitlab_url():
        return os.getenv('GITLAB_URL')

    @staticmethod
    def gitlab_project_id():
        return os.getenv('GITLAB_PROJECT')

    @staticmethod
    def gitlab_branch():
        return os.getenv('GITLAB_BRANCH')
