from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from .exceptions import BusinessRuleViolation


class BusinessRule(ABC):
    __slots__ = ()

    @abstractmethod
    def is_broken(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError

    def validate(self) -> None:
        if self.is_broken():
            raise BusinessRuleViolation(self.message)


class CompositeBusinessRule(BusinessRule):
    __slots__ = ("_rules",)

    def __init__(self, *rules: BusinessRule) -> None:
        self._rules: Sequence[BusinessRule] = rules

    @property
    def rules(self) -> Sequence[BusinessRule]:
        return self._rules

    @property
    def message(self) -> str:
        for rule in self._rules:
            if rule.is_broken():
                return rule.message
        return ""


class AnyBusinessRule(CompositeBusinessRule):
    __slots__ = ()

    def is_broken(self) -> bool:
        return all(rule.is_broken() for rule in self.rules)


class AllBusinessRule(CompositeBusinessRule):
    __slots__ = ()

    def is_broken(self) -> bool:
        return any(rule.is_broken() for rule in self.rules)