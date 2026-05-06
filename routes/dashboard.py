from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Shipment, CourierStatusEnum
from schemas import DashboardOut, BranchSummary
from routes.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

BRANCHES = [
    "Zirakpur", "Barwala", "Sonipat", "Kanpur", "Varanasi",
    "Odisha", "Raipur", "Patna", "Howrah", "Delhi"
]


@router.get("/", response_model=DashboardOut)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns summary statistics for the dashboard.

    - HEAD OFFICE: gets counts for ALL branches + per-branch breakdown
    - BRANCH: gets counts for their branch only, no branch breakdown
    """
    # Base query — filtered by branch for branch users
    query = db.query(Shipment)
    if current_user.role == "branch":
        query = query.filter(Shipment.branch_name == current_user.branch)

    all_shipments = query.all()

    # Count by status
    def count(status_val):
        return sum(1 for s in all_shipments if s.courier_status == status_val)

    delayed_list = [
        {"branch": s.branch_name, "awb": s.awb_number, "party": s.party_name}
        for s in all_shipments if s.courier_status == CourierStatusEnum.delayed
    ]

    # Per-branch breakdown (head office only)
    branch_summary = []
    if current_user.role == "head":
        for branch in BRANCHES:
            branch_data = [s for s in all_shipments if s.branch_name == branch]
            if branch_data:
                branch_summary.append(BranchSummary(
                    branch_name      = branch,
                    total            = len(branch_data),
                    in_transit       = sum(1 for s in branch_data if s.courier_status == CourierStatusEnum.in_transit),
                    delivered        = sum(1 for s in branch_data if s.courier_status == CourierStatusEnum.delivered),
                    out_for_delivery = sum(1 for s in branch_data if s.courier_status == CourierStatusEnum.out_for_delivery),
                    delayed          = sum(1 for s in branch_data if s.courier_status == CourierStatusEnum.delayed),
                    rto              = sum(1 for s in branch_data if s.courier_status == CourierStatusEnum.rto),
                    pending          = sum(1 for s in branch_data if s.courier_status == CourierStatusEnum.pending),
                ))

    return DashboardOut(
        total             = len(all_shipments),
        in_transit        = count(CourierStatusEnum.in_transit),
        delivered         = count(CourierStatusEnum.delivered),
        out_for_delivery  = count(CourierStatusEnum.out_for_delivery),
        delayed           = count(CourierStatusEnum.delayed),
        rto_pending       = count(CourierStatusEnum.rto) + count(CourierStatusEnum.pending),
        delayed_shipments = delayed_list,
        branch_summary    = branch_summary,
    )
