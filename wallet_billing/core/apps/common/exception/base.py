from dataclasses import dataclass


@dataclass(eq=False)
class ServiceException(Exception):
    @property
    def message(self):
        return "Application exception occurred"

    @property
    def status_code(self):
        return 500