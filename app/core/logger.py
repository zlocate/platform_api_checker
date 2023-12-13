import sentry_sdk


class SingletonMetaLogger(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class CustomLogger(metaclass=SingletonMetaLogger):
    def __init__(self):
        sentry_sdk.init(
            dsn="https://b0f3a40208402c81879a79fe8bab4992@o4506372955176960.ingest.sentry.io/4506372988272640",
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )

    def message(self, msg = ""):
        print(msg)
        sentry_sdk.capture_message(msg)

    def error(self, msg = ""):
        print(msg)
        sentry_sdk.capture_exception(msg)