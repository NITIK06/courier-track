from database import SessionLocal, engine, Base
from models import User, Shipment, CourierNameEnum, CourierStatusEnum, RoleEnum
from auth import hash_password
from datetime import date


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # ── USERS ──
    users_data = [
        ("HO","Head Office","1234",RoleEnum.head,None),
        ("ZKP","Zirakpur Branch","1234",RoleEnum.branch,"Zirakpur"),
        ("BWL","Barwala Branch","1234",RoleEnum.branch,"Barwala"),
        ("SNP","Sonipat Branch","1234",RoleEnum.branch,"Sonipat"),
        ("KNP","Kanpur Branch","1234",RoleEnum.branch,"Kanpur"),
        ("VNS","Varanasi Branch","1234",RoleEnum.branch,"Varanasi"),
        ("ODS","Odisha Branch","1234",RoleEnum.branch,"Odisha"),
        ("RPR","Raipur Branch","1234",RoleEnum.branch,"Raipur"),
        ("PTN","Patna Branch","1234",RoleEnum.branch,"Patna"),
        ("HWR","Howrah Branch","1234",RoleEnum.branch,"Howrah"),
        ("DLH","Delhi Branch","1234",RoleEnum.branch,"Delhi"),
    ]

    print("Creating users...")
    for code, name, pwd, role, branch in users_data:
        existing = db.query(User).filter(User.branch_code == code).first()
        if not existing:
            db.add(User(
                branch_code=code,
                branch_name=name,
                password_hash=hash_password(pwd),
                role=role,
                branch=branch
            ))

    db.commit()
    print("Users created.\n")

    # ── SHIPMENTS ──
    shipments_data = [
        ("Zirakpur","PC-001","Raj Traders","9876543210",date(2025,3,10),"INV-1001",42000,5.2,"140603","Zirakpur","Punjab",CourierNameEnum.blue_dart,"AWB-1001",date(2025,3,11),3,date(2025,3,14),date(2025,3,14),"",CourierStatusEnum.delivered),
    ]

    print("Creating shipments...")
    for row in shipments_data:
        (branch, pcode, pname, mobile, inv_date, inv_no, inv_val, weight,
         pin, city, state, courier, awb, dispatch, tat, expected, actual, policy, st) = row

        existing = db.query(Shipment).filter(Shipment.awb_number == awb).first()
        if not existing:
            db.add(Shipment(
                branch_name=branch, party_code=pcode, party_name=pname, mobile=mobile,
                invoice_date=inv_date, invoice_number=inv_no, invoice_value=inv_val,
                final_weight=weight, pin_code=pin, city=city, state=state,
                courier_name=courier, awb_number=awb, dispatch_date=dispatch,
                branch_tat=tat, expected_delivery=expected, actual_delivery=actual,
                policy_number=policy or None, courier_status=st
            ))

    db.commit()
    db.close()
    print("Seeding Done ✅")