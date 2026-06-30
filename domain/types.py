from __future__ import annotations

from typing import NewType
from uuid import UUID

"""
Domain primitive identifier types.

These aliases provide stronger semantic meaning than raw UUID values while
remaining lightweight and infrastructure-agnostic.

They intentionally do not encode persistence or transport concerns.
"""

AggregateId = NewType("AggregateId", UUID)
EntityId = NewType("EntityId", UUID)

TenantId = NewType("TenantId", UUID)
UserId = NewType("UserId", UUID)

ConversationId = NewType("ConversationId", UUID)
MessageId = NewType("MessageId", UUID)

MissionId = NewType("MissionId", UUID)

EventId = NewType("EventId", UUID)
CorrelationId = NewType("CorrelationId", UUID)
CausationId = NewType("CausationId", UUID)