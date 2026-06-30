from __future__ import annotations

from enum import StrEnum


class DomainConstants(StrEnum):
    """
    Domain-wide immutable constants.

    These values represent semantic constants of the Domain itself.
    They must not contain configuration values, environment settings,
    infrastructure details or feature flags.
    """

    VERSION = "1.0"