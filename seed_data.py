"""
seed_data.py — Run this ONCE after setting up MySQL to:
  1. Create the database tables
  2. Insert all 11 users (HO + 10 branches)
  3. Insert sample shipment data

Run with:
    python seed_data.py
"""

from database import SessionLocal, engine, Base
from models import User, Shipment, CourierNameEnum, CourierStatusEnum, RoleEnum
from auth import hash_password
from datetime import date

Base.metadata.create_all(bind=engine)
db = SessionLocal()


# ── Step 1: Create users ──────────────────────────────────────────────────────

users_data = [
    # (branch_code, branch_name, password, role, branch)
    ("HO",  "Head Office",      "1234", RoleEnum.head,   None),
    ("ZKP", "Zirakpur Branch",  "1234", RoleEnum.branch, "Zirakpur"),
    ("BWL", "Barwala Branch",   "1234", RoleEnum.branch, "Barwala"),
    ("SNP", "Sonipat Branch",   "1234", RoleEnum.branch, "Sonipat"),
    ("KNP", "Kanpur Branch",    "1234", RoleEnum.branch, "Kanpur"),
    ("VNS", "Varanasi Branch",  "1234", RoleEnum.branch, "Varanasi"),
    ("ODS", "Odisha Branch",    "1234", RoleEnum.branch, "Odisha"),
    ("RPR", "Raipur Branch",    "1234", RoleEnum.branch, "Raipur"),
    ("PTN", "Patna Branch",     "1234", RoleEnum.branch, "Patna"),
    ("HWR", "Howrah Branch",    "1234", RoleEnum.branch, "Howrah"),
    ("DLH", "Delhi Branch",     "1234", RoleEnum.branch, "Delhi"),
]

print("Creating users...")
for code, name, pwd, role, branch in users_data:
    existing = db.query(User).filter(User.branch_code == code).first()
    if not existing:
        db.add(User(
            branch_code   = code,
            branch_name   = name,
            password_hash = hash_password(pwd),
            role          = role,
            branch        = branch
        ))
        print(f"  Created user: {code} ({name})")
    else:
        print(f"  Skipped (already exists): {code}")

db.commit()
print("Users created.\n")


# ── Step 2: Create sample shipments ──────────────────────────────────────────

shipments_data = [
    ("Zirakpur",  "PC-001", "Raj Traders",          "9876543210", date(2025,3,10), "INV-1001", 42000,  5.2,  "140603", "Zirakpur",   "Punjab",    CourierNameEnum.blue_dart,         "AWB-1001", date(2025,3,11), 3, date(2025,3,14), date(2025,3,14), "",          CourierStatusEnum.delivered),
    ("Barwala",   "PC-002", "Sharma Enterprises",   "9812345678", date(2025,3,11), "INV-1002", 75000,  8.5,  "125121", "Barwala",    "Haryana",   CourierNameEnum.safe_express,      "AWB-1002", date(2025,3,12), 4, date(2025,3,16), None,            "POL-5521",  CourierStatusEnum.in_transit),
    ("Sonipat",   "PC-003", "Gupta & Sons",         "9765432100", date(2025,3,10), "INV-1003", 28000,  3.1,  "131001", "Sonipat",    "Haryana",   CourierNameEnum.dtdc_express,      "AWB-1003", date(2025,3,11), 2, date(2025,3,13), date(2025,3,13), "",          CourierStatusEnum.delivered),
    ("Kanpur",    "PC-004", "Modi Fabrics",         "9898989898", date(2025,3,9),  "INV-1004", 55000,  12.0, "208001", "Kanpur",     "UP",        CourierNameEnum.ship_rocket,       "AWB-1043", date(2025,3,10), 3, date(2025,3,13), None,            "POL-5534",  CourierStatusEnum.delayed),
    ("Varanasi",  "PC-005", "Kashi Exports",        "9811223344", date(2025,3,12), "INV-1005", 33000,  7.8,  "221001", "Varanasi",   "UP",        CourierNameEnum.jet_line,          "AWB-1005", date(2025,3,13), 4, date(2025,3,17), None,            "",          CourierStatusEnum.out_for_delivery),
    ("Odisha",    "PC-006", "Patra Distributors",   "9700112233", date(2025,3,11), "INV-1006", 61000,  9.0,  "751001", "Bhubaneswar","Odisha",    CourierNameEnum.blue_dart_surface, "AWB-1006", date(2025,3,12), 5, date(2025,3,17), None,            "POL-5540",  CourierStatusEnum.in_transit),
    ("Raipur",    "PC-007", "Singh & Co",           "9654321098", date(2025,3,10), "INV-1007", 19000,  2.5,  "492001", "Raipur",     "CG",        CourierNameEnum.dtdc_ltl,          "AWB-1007", date(2025,3,11), 3, date(2025,3,14), date(2025,3,15), "",          CourierStatusEnum.delivered),
    ("Patna",     "PC-008", "Bihar Goods House",    "9543210987", date(2025,3,10), "INV-1008", 48000,  6.3,  "800001", "Patna",      "Bihar",     CourierNameEnum.bharat_dart,       "AWB-1017", date(2025,3,11), 4, date(2025,3,15), None,            "",          CourierStatusEnum.delayed),
    ("Howrah",    "PC-009", "Bengal Merchants",     "9432109876", date(2025,3,11), "INV-1009", 82000,  14.2, "711101", "Howrah",     "WB",        CourierNameEnum.blue_dart_dp,      "AWB-1021", date(2025,3,12), 3, date(2025,3,15), None,            "POL-5557",  CourierStatusEnum.delayed),
    ("Delhi",     "PC-010", "Capital Traders",      "9321098765", date(2025,3,12), "INV-1010", 37000,  4.5,  "110001", "Delhi",      "Delhi",     CourierNameEnum.ship_rocket,       "AWB-1010", date(2025,3,13), 2, date(2025,3,15), None,            "",          CourierStatusEnum.pending),
    ("Delhi",     "PC-011", "DelhiTech Supplies",   "9310987654", date(2025,3,13), "INV-1011", 95000,  11.0, "110005", "Delhi",      "Delhi",     CourierNameEnum.safe_express,      "AWB-1011", date(2025,3,14), 3, date(2025,3,17), None,            "POL-5560",  CourierStatusEnum.in_transit),
]

print("Creating sample shipments...")
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
        print(f"  Added: {awb} ({branch})")
    else:
        print(f"  Skipped (exists): {awb}")

db.commit()
db.close()
print("\nAll done! You can now run: uvicorn main:app --reload")
