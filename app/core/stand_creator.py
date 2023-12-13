from enum import Enum

from app.clients.gitlab_client import GitlabClient
from app.core.logger import CustomLogger
from app.models.create_stand_request import CreateStandRequest
import threading


class PipelineAction(Enum):
    RESTART = 'перезапуск'
    WAIT = 'ждем'
    READY = 'готово'


class SingletonMetaStandCreator(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class PipelinesThreadSafeDict:
    def __init__(self):
        self._dict = {}
        self.__lock = threading.Lock()

    def getitem(self, key):
        with self.__lock:
            return self._dict[key]

    def setitem(self, key, value):
        with self.__lock:
            self._dict[key] = value

    def delitem(self, key):
        with self.__lock:
            del self._dict[key]

    def getkeys(self):
        with self.__lock:
            return self._dict.keys()


class StandCreator(metaclass=SingletonMetaStandCreator):
    def __init__(self, gitlab_client: GitlabClient):
        self.__gitlab_client = gitlab_client
        self.__pipelines = PipelinesThreadSafeDict()
        self.__logger = CustomLogger()

    def create_stand_handler(self, request: CreateStandRequest):
        self.__logger.message(f"Начинаем обработку запроса {request}")
        if request in self.__pipelines.getkeys():
            self.__logger.message(f"Запрос {request} был ранее получен")
            pipeline_id = self.__pipelines.getitem(request)
            status = self.is_pipeline_finished(pipeline_id)
            self.__logger.message(f"Статус пайплайна по запросу {request} {status}")
            if status == PipelineAction.WAIT:
                self.__logger.message(f"Пайплайн {pipeline_id} ожидает завершения выполнения")
                return
            elif status == PipelineAction.READY:
                domain = self.generate_domain(request)
                self.__logger.message(
                    f"Пайплайн {pipeline_id} по запросу {request} завершен. Сгенерирован стенд {domain}")
                return domain
        pipeline_id = self.__gitlab_client.run_create_stand_pipeline(request)
        self.__logger.message(f"Пайплайн {pipeline_id} на {request} запущен")
        self.__pipelines.setitem(request, pipeline_id)
        return

    def is_pipeline_finished(self, pipeline_id) -> PipelineAction:
        status = self.__gitlab_client.check_pipeline_status(pipeline_id)
        if status in ['pending', 'running', 'created']:
            return PipelineAction.WAIT
        if status in ['failed', 'canceled', 'skipped']:
            return PipelineAction.RESTART
        return PipelineAction.READY

    def generate_domain(self, request: CreateStandRequest):

        if request.task_number == 'task1':
            return f"{request.task_number}-alert-{request.yuid}-{request.stand_number}.seccheck.ru".lower()
        elif request.task_number == 'task2':
            return f"{request.task_number}-blndsqli-{request.yuid}-{request.stand_number}.seccheck.ru".lower()
        elif request.task_number == 'task3':
            return f"{request.task_number}-rpass-{request.yuid}-{request.stand_number}.seccheck.ru".lower()
        elif request.task_number == 'task4':
            return f"{request.task_number}-xxe-{request.yuid}-{request.stand_number}.seccheck.ru".lower()
        elif request.task_number == 'task5':
            return f"{request.task_number}-images-{request.yuid}-{request.stand_number}.seccheck.ru".lower()
        else:
            return ""
