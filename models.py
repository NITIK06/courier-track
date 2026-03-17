from sqlalchemy import (
    Column, Integer, String, Float, Date,
    DateTime, Enum, ForeignKey, func
)
from sqlalchemy.orm import relationship
from database import Base
import enum


# ── Enums (match your dropdown values exactly) ──────────────────────────────

class CourierNameEnum(str, enum.Enum):
    blue_dart         = "Blue Dart"
    ship_rocket       = "Ship Rocket"
    safe_express      = "Safe Express"
    jet_line          = "Jet Line"
    dtdc_ltl          = "DTDC LTL"
    blue_dart_dp      = "Blue Dart DP"
    blue_dart_surface = "Blue Dart Surface"
    bharat_dart       = "Bharat Dart"
    dtdc_express      = "DTDC EXPRESS"


class CourierStatusEnum(str, enum.Enum):
    in_transit       = "In Transit"
    delivered        = "Delivered"
    out_for_delivery = "Out for Delivery"
    pending          = "Pending"
    delayed          = "Delayed"
    rto              = "RTO"


class RoleEnum(str, enum.Enum):
    head   = "head"
    branch = "branch"


# ── Table 1: users ────────────────────────────────────────────────────────────
# Stores login credentials for head office and each branch.

class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    branch_code   = Column(String(10), unique=True, nullable=False)   # e.g. "ZKP", "HO"
    branch_name   = Column(String(100), nullable=False)               # e.g. "Zirakpur Branch"
    password_hash = Column(String(255), nullable=False)               # bcrypt hashed
    role          = Column(Enum(RoleEnum), nullable=False)            # "head" or "branch"
    branch        = Column(String(100), nullable=True)                # NULL for head office


# ── Table 2: shipments ────────────────────────────────────────────────────────
# One row per shipment entry. Branches add rows; branches update status.

class Shipment(Base):
    __tablename__ = "shipments"

    id             = Column(Integer, primary_key=True, index=True)

    # Branch info
    branch_name    = Column(String(100), nullable=False)
    party_code     = Column(String(50),  nullable=False)
    party_name     = Column(String(200), nullable=False)
    mobile         = Column(String(15),  nullable=False)

    # Invoice details
    invoice_date   = Column(Date,        nullable=False)
    invoice_number = Column(String(50),  nullable=False)
    invoice_value  = Column(Float,       nullable=False)
    final_weight   = Column(Float,       nullable=False)

    # Address
    pin_code       = Column(String(10),  nullable=False)
    city           = Column(String(100), nullable=False)
    state          = Column(String(100), nullable=False)

    # Courier info
    courier_name   = Column(Enum(CourierNameEnum), nullable=False)
    awb_number     = Column(String(100), unique=True, nullable=False)
    dispatch_date  = Column(Date,        nullable=False)
    branch_tat     = Column(Integer,     nullable=True)
    expected_delivery = Column(Date,     nullable=True)
    actual_delivery   = Column(Date,     nullable=True)

    # Policy (mandatory if invoice_value > 50000)
    policy_number  = Column(String(100), nullable=True)

    # Status (branches can update this)
    courier_status = Column(Enum(CourierStatusEnum), nullable=False, default=CourierStatusEnum.pending)

    # Timestamps
    created_at     = Column(DateTime, server_default=func.now())
    updated_at     = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Which user (branch) created this entry
    created_by     = Column(Integer, ForeignKey("users.id"), nullable=True)
    creator        = relationship("User")
