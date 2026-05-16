"""Core data models for financial services.

Defines the primary data structures used across the financial services
platform, including accounts, transactions, and portfolios.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
import uuid


class AccountType(str, Enum):
    """Supported account types."""
    CHECKING = "checking"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    RETIREMENT = "retirement"
    CREDIT = "credit"


class TransactionType(str, Enum):
    """Types of financial transactions."""
    DEBIT = "debit"
    CREDIT = "credit"
    TRANSFER = "transfer"
    FEE = "fee"
    INTEREST = "interest"
    DIVIDEND = "dividend"


class TransactionStatus(str, Enum):
    """Status of a financial transaction."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"


@dataclass
class Account:
    """Represents a financial account."""

    owner_id: str
    account_type: AccountType
    currency: str = "USD"
    balance: Decimal = field(default_factory=lambda: Decimal("0.00"))
    account_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    nickname: Optional[str] = None

    def __post_init__(self):
        # Ensure balance is always a Decimal for precision
        if not isinstance(self.balance, Decimal):
            self.balance = Decimal(str(self.balance))

    def can_debit(self, amount: Decimal) -> bool:
        """Check whether the account has sufficient funds for a debit."""
        if self.account_type == AccountType.CREDIT:
            return True  # Credit accounts handle limits separately
        return self.balance >= amount


@dataclass
class Transaction:
    """Represents a single financial transaction."""

    account_id: str
    transaction_type: TransactionType
    amount: Decimal
    description: str
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TransactionStatus = TransactionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    reference_id: Optional[str] = None  # External reference (e.g., wire transfer ID)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))
        if self.amount <= Decimal("0"):
            raise ValueError("Transaction amount must be positive.")

    def complete(self) -> None:
        """Mark the transaction as completed."""
        self.status = TransactionStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    def fail(self) -> None:
        """Mark the transaction as failed."""
        self.status = TransactionStatus.FAILED
        self.completed_at = datetime.utcnow()


@dataclass
class PortfolioPosition:
    """Represents a holding within an investment portfolio."""

    account_id: str
    symbol: str
    quantity: Decimal
    average_cost_basis: Decimal
    position_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    last_updated: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not isinstance(self.quantity, Decimal):
            self.quantity = Decimal(str(self.quantity))
        if not isinstance(self.average_cost_basis, Decimal):
            self.average_cost_basis = Decimal(str(self.average_cost_basis))

    def market_value(self, current_price: Decimal) -> Decimal:
        """Calculate the current market value of this position."""
        return self.quantity * current_price

    def unrealized_gain_loss(self, current_price: Decimal) -> Decimal:
        """Calculate unrealized gain or loss at the given market price."""
        return self.market_value(current_price) - (self.quantity * self.average_cost_basis)
