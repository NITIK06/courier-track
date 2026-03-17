from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from models import CourierNameEnum, CourierStatusEnum, RoleEnum


# ── Auth Schemas ─────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    branch_code: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    branch_code: str
    branch_name: str
    role: RoleEnum
    branch: Optional[str] = None


# ── Shipment Schemas ──────────────────────────────────────────────────────────

class ShipmentCreate(BaseModel):
    """Used when a branch submits a new shipment entry (POST /shipments)"""
    party_code:        str
    party_name:        str
    mobile:            str
    invoice_date:      date
    invoice_number:    str
    invoice_value:     float
    final_weight:      float
    pin_code:          str
    city:              str
    state:             str
    courier_name:      CourierNameEnum
    awb_number:        str
    dispatch_date:     date
    branch_tat:        Optional[int]  = None
    expected_delivery: Optional[date] = None
    actual_delivery:   Optional[date] = None
    policy_number:     Optional[str]  = None
    courier_status:    CourierStatusEnum

    @field_validator("policy_number")
    @classmethod
    def policy_required_above_50k(cls, v, info):
        """Policy number is mandatory if invoice value exceeds 50,000"""
        invoice_value = info.data.get("invoice_value", 0)
        if invoice_value > 50000 and not v:
            raise ValueError("Policy number is required when invoice value exceeds ₹50,000")
        return v

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Mobile number must be exactly 10 digits")
        return v


class StatusUpdate(BaseModel):
    """Used when a branch updates only the courier status (PATCH /shipments/{id}/status)"""
    courier_status:  CourierStatusEnum
    actual_delivery: Optional[date] = None


class ShipmentOut(BaseModel):
    """What the API returns when listing shipments"""
    id:                int
    branch_name:       str
    party_code:        str
    party_name:        str
    mobile:            str
    invoice_date:      date
    invoice_number:    str
    invoice_value:     float
    final_weight:      float
    pin_code:          str
    city:              str
    state:             str
    courier_name:      str
    awb_number:        str
    dispatch_date:     date
    branch_tat:        Optional[int]
    expected_delivery: Optional[date]
    actual_delivery:   Optional[date]
    policy_number:     Optional[str]
    courier_status:    str
    created_at:        Optional[datetime]
    updated_at:        Optional[datetime]

    class Config:
        from_attributes = True


# ── Dashboard Schema ──────────────────────────────────────────────────────────

class BranchSummary(BaseModel):
    branch_name:      str
    total:            int
    in_transit:       int
    delivered:        int
    out_for_delivery: int
    delayed:          int
    rto:              int
    pending:          int


class DashboardOut(BaseModel):
    total:            int
    in_transit:       int
    delivered:        int
    out_for_delivery: int
    delayed:          int
    rto_pending:      int
    delayed_shipments: list[dict]         # list of {branch, awb} for alerts
    branch_summary:   list[BranchSummary] # only populated for head office
