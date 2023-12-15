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

    @staticmethod   
    def get_basic_auth_username():
        return os.getenv('BASIC_AUTH_USERNAME')
    
    @staticmethod 
    def get_basic_auth_password():
        return os.getenv('BASIC_AUTH_PASSWORD')
    
    @staticmethod 
    def get_is_basic_auth_required():
        is_basic_auth_required = os.getenv('IS_BASIC_AUTH_REQUIRED')
        return str(is_basic_auth_required).lower() == 'true'