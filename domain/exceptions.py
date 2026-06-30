from __future__ import annotations


class DomainError(Exception):
    """
    Base exception for all domain-level errors.

    Every exception raised from the Domain should inherit from this type,
    allowing the Application layer to translate them into transport-specific
    responses (HTTP, CLI, messaging, etc.) without coupling the Domain to
    any framework.
    """

    __slots__ = ()


class ValidationError(DomainError):
    """
    Raised when a Value Object or Entity receives invalid data.
    """

    __slots__ = ()


class BusinessRuleViolation(DomainError):
    """
    Raised when a business invariant is violated.
    """

    __slots__ = ()


class EntityNotFound(DomainError):
    """
    Raised when a requested Entity or Aggregate cannot be found.
    """

    __slots__ = ()


class ConcurrencyError(DomainError):
    """
    Raised when optimistic concurrency detects conflicting modifications.
    """

    __slots__ = ()