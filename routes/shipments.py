from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User, Shipment
from schemas import ShipmentCreate, ShipmentOut, StatusUpdate
from routes.auth import get_current_user, require_branch
from models import RoleEnum
router = APIRouter(prefix="/shipments", tags=["Shipments"])


@router.get("/", response_model=list[ShipmentOut])
def get_shipments(
    branch:  Optional[str] = Query(None, description="Filter by branch name"),
    status:  Optional[str] = Query(None, description="Filter by courier status"),
    courier: Optional[str] = Query(None, description="Filter by courier name"),
    search:  Optional[str] = Query(None, description="Search by AWB or party name"),
    db:      Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get shipments list.

    - HEAD OFFICE: sees all branches. Can filter by branch/status/courier/search.
    - BRANCH USER: sees ONLY their own branch shipments. branch filter is ignored.

    Example:
        GET /shipments?status=Delayed
        GET /shipments?branch=Kanpur&courier=Blue+Dart
    """
    query = db.query(Shipment)

    # KEY RULE: Branch users only see their own data
    if current_user.role == "branch":
        query = query.filter(Shipment.branch_name == current_user.branch)
    elif branch:
        query = query.filter(Shipment.branch_name == branch)

    if status:
        query = query.filter(Shipment.courier_status == status)
    if courier:
        query = query.filter(Shipment.courier_name == courier)
    if search:
        query = query.filter(
            Shipment.awb_number.ilike(f"%{search}%") |
            Shipment.party_name.ilike(f"%{search}%") |
            Shipment.invoice_number.ilike(f"%{search}%")
        )

    return query.order_by(Shipment.created_at.desc()).all()


@router.post("/", response_model=ShipmentOut, status_code=status.HTTP_201_CREATED)
def add_shipment(
    data: ShipmentCreate,
    db:   Session = Depends(get_db),
    current_user: User = Depends(require_branch)   # blocks head office
):
    """
    Add a new shipment entry. BRANCH ONLY.

    The branch_name is taken from the logged-in user's profile —
    branch cannot submit entries for other branches.

    Validation:
        - Policy number required if invoice_value > 50,000
        - AWB number must be unique
    """
    # Check AWB is not duplicate
    existing = db.query(Shipment).filter(Shipment.awb_number == data.awb_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"AWB number '{data.awb_number}' already exists in the system"
        )

    shipment = Shipment(
        branch_name       = current_user.branch,   # auto-set from token
        party_code        = data.party_code,
        party_name        = data.party_name,
        mobile            = data.mobile,
        invoice_date      = data.invoice_date,
        invoice_number    = data.invoice_number,
        invoice_value     = data.invoice_value,
        final_weight      = data.final_weight,
        pin_code          = data.pin_code,
        city              = data.city,
        state             = data.state,
        courier_name      = data.courier_name,
        awb_number        = data.awb_number,
        dispatch_date     = data.dispatch_date,
        branch_tat        = data.branch_tat,
        expected_delivery = data.expected_delivery,
        actual_delivery   = data.actual_delivery,
        policy_number     = data.policy_number,
        courier_status    = data.courier_status,
        created_by        = current_user.id,
    )

    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment


@router.patch("/{shipment_id}/status", response_model=ShipmentOut)
def update_status(
    shipment_id: int,
    data:        StatusUpdate,
    db:          Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    if current_user.role != RoleEnum.head and shipment.branch_name != current_user.branch:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update shipments belonging to your branch"
        )

    if data.courier_status is not None:
        shipment.courier_status = data.courier_status
    if data.actual_delivery is not None:
        shipment.actual_delivery = data.actual_delivery

    db.commit()
    db.refresh(shipment)
    return shipment