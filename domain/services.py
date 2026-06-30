from __future__ import annotations

from abc import ABC, abstractmethod

from .aura import Aura
from .conversation import Conversation
from .mission import Mission
from .progress import Progress


class DomainService(ABC):
    """
    Base class for all Domain Services.

    Domain services encapsulate business operations that do not naturally
    belong to a single Entity, Aggregate or Value Object.

    They must remain pure domain abstractions and never depend on
    infrastructure concerns.
    """

    __slots__ = ()


class AuraAnalysisService(DomainService):
    """
    Produces an Aura from a Conversation according to domain rules.
    """

    __slots__ = ()

    @abstractmethod
    async def analyze(
        self,
        conversation: Conversation,
    ) -> Aura:
        raise NotImplementedError


class MissionGenerationService(DomainService):
    """
    Generates the set of Missions required for a given Aura.
    """

    __slots__ = ()

    @abstractmethod
    async def generate(
        self,
        aura: Aura,
    ) -> list[Mission]:
        raise NotImplementedError


class ProgressCalculationService(DomainService):
    """
    Calculates overall Progress from the current Mission collection.
    """

    __slots__ = ()

    @abstractmethod
    def calculate(
        self,
        missions: list[Mission],
    ) -> Progress:
        raise NotImplementedError