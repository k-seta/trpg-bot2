from abc import ABCMeta, abstractmethod


class ABCArg(metaclass=ABCMeta):
    @abstractmethod
    def value(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def calc_value(self) -> str:
        raise NotImplementedError()
