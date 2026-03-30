from database import SessionLocal, engine, Base
from models import User, Shipment, CourierNameEnum, CourierStatusEnum, RoleEnum
from routes.auth import hash_password
from datetime import date


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # ── USERS ──
    users_data = [
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
        ("Zirakpur", "PC-001", "Raj Traders",      "9876543210", date(2025,3,10), "INV-1001", 42000,  5.2, "140603", "Zirakpur",  "Punjab",      CourierNameEnum.blue_dart,         "AWB-1001", date(2025,3,11), 3, date(2025,3,14), date(2025,3,14), "",           CourierStatusEnum.delivered),
        ("Zirakpur", "PC-002", "Singh Enterprises","9812345670", date(2025,3,12), "INV-1002", 28000,  3.5, "140603", "Zirakpur",  "Punjab",      CourierNameEnum.dtdc_express,      "AWB-1002", date(2025,3,12), 4, date(2025,3,16), None,           "",           CourierStatusEnum.in_transit),
        ("Zirakpur", "PC-003", "Pawan Goods",      "9801234567", date(2025,3,13), "INV-1003", 15000,  2.0, "140603", "Zirakpur",  "Punjab",      CourierNameEnum.safe_express,      "AWB-1003", date(2025,3,13), 3, date(2025,3,16), None,           "",           CourierStatusEnum.delayed),

        ("Kanpur",   "PC-101", "Kapoor Textiles",  "9988776655", date(2025,3,9),  "INV-2001", 75000,  8.0, "208001", "Kanpur",    "Uttar Pradesh",CourierNameEnum.blue_dart,        "AWB-2001", date(2025,3,10), 5, date(2025,3,15), date(2025,3,15), "POL-9901",   CourierStatusEnum.delivered),
        ("Kanpur",   "PC-102", "Mehta Bros",       "9977665544", date(2025,3,11), "INV-2002", 32000,  4.5, "208002", "Kanpur",    "Uttar Pradesh",CourierNameEnum.ship_rocket,      "AWB-2002", date(2025,3,11), 4, date(2025,3,15), None,           "",           CourierStatusEnum.out_for_delivery),
        ("Kanpur",   "PC-103", "Gupta Store",      "9966554433", date(2025,3,12), "INV-2003", 18000,  3.0, "208003", "Kanpur",    "Uttar Pradesh",CourierNameEnum.dtdc_ltl,         "AWB-2003", date(2025,3,12), 3, date(2025,3,15), None,           "",           CourierStatusEnum.in_transit),

        ("Delhi",    "PC-201", "Delhi Distributors","9811223344",date(2025,3,8),  "INV-3001", 95000, 12.0, "110001", "New Delhi", "Delhi",       CourierNameEnum.blue_dart_surface, "AWB-3001", date(2025,3,9),  5, date(2025,3,14), date(2025,3,14), "POL-8801",   CourierStatusEnum.delivered),
        ("Delhi",    "PC-202", "Sharma Trading",   "9822334455", date(2025,3,11), "INV-3002", 44000,  6.5, "110002", "New Delhi", "Delhi",       CourierNameEnum.safe_express,      "AWB-3002", date(2025,3,11), 4, date(2025,3,15), None,           "",           CourierStatusEnum.in_transit),
        ("Delhi",    "PC-203", "Verma Logistics",  "9833445566", date(2025,3,13), "INV-3003", 21000,  3.8, "110003", "New Delhi", "Delhi",       CourierNameEnum.jet_line,          "AWB-3003", date(2025,3,13), 3, date(2025,3,16), None,           "",           CourierStatusEnum.pending),

        ("Varanasi", "PC-301", "Banaras Sarees",   "9712345678", date(2025,3,10), "INV-4001", 62000,  7.0, "221001", "Varanasi",  "Uttar Pradesh",CourierNameEnum.blue_dart_dp,     "AWB-4001", date(2025,3,10), 5, date(2025,3,15), None,           "POL-7701",   CourierStatusEnum.delayed),
        ("Varanasi", "PC-302", "Kashi Traders",    "9723456789", date(2025,3,12), "INV-4002", 29000,  4.2, "221002", "Varanasi",  "Uttar Pradesh",CourierNameEnum.dtdc_express,     "AWB-4002", date(2025,3,12), 4, date(2025,3,16), None,           "",           CourierStatusEnum.in_transit),

        ("Patna",    "PC-401", "Bihar Merchants",  "9631234567", date(2025,3,9),  "INV-5001", 38000,  5.5, "800001", "Patna",     "Bihar",       CourierNameEnum.safe_express,      "AWB-5001", date(2025,3,10), 4, date(2025,3,14), date(2025,3,15), "",           CourierStatusEnum.delivered),
        ("Patna",    "PC-402", "Patna Goods",      "9642345678", date(2025,3,13), "INV-5002", 17000,  2.8, "800002", "Patna",     "Bihar",       CourierNameEnum.ship_rocket,       "AWB-5002", date(2025,3,13), 3, date(2025,3,16), None,           "",           CourierStatusEnum.in_transit),

        ("Howrah",   "PC-501", "Bengal Traders",   "9831234567", date(2025,3,8),  "INV-6001", 55000,  9.0, "711101", "Howrah",    "West Bengal", CourierNameEnum.blue_dart,         "AWB-6001", date(2025,3,9),  5, date(2025,3,14), None,           "POL-6601",   CourierStatusEnum.rto),
        ("Howrah",   "PC-502", "Kolkata Supplies", "9842345678", date(2025,3,12), "INV-6002", 33000,  4.8, "711102", "Howrah",    "West Bengal", CourierNameEnum.dtdc_ltl,          "AWB-6002", date(2025,3,12), 4, date(2025,3,16), None,           "",           CourierStatusEnum.in_transit),

        ("Odisha",   "PC-601", "Orissa Exports",   "9777123456", date(2025,3,10), "INV-7001", 48000,  6.2, "751001", "Bhubaneswar","Odisha",     CourierNameEnum.safe_express,      "AWB-7001", date(2025,3,11), 5, date(2025,3,16), None,           "",           CourierStatusEnum.in_transit),
        ("Odisha",   "PC-602", "Puri Handicrafts", "9788234567", date(2025,3,13), "INV-7002", 22000,  3.2, "752001", "Puri",      "Odisha",      CourierNameEnum.bharat_dart,       "AWB-7002", date(2025,3,13), 3, date(2025,3,16), None,           "",           CourierStatusEnum.pending),

        ("Raipur",   "PC-701", "CG Traders",       "7712345678", date(2025,3,9),  "INV-8001", 41000,  5.8, "492001", "Raipur",    "Chhattisgarh",CourierNameEnum.blue_dart_surface,"AWB-8001", date(2025,3,10), 4, date(2025,3,14), date(2025,3,14), "",           CourierStatusEnum.delivered),
        ("Raipur",   "PC-702", "Raipur Stores",    "7723456789", date(2025,3,12), "INV-8002", 26000,  3.6, "492002", "Raipur",    "Chhattisgarh",CourierNameEnum.ship_rocket,      "AWB-8002", date(2025,3,12), 4, date(2025,3,16), None,           "",           CourierStatusEnum.delayed),

        ("Sonipat",  "PC-801", "Haryana Agro",     "9991234567", date(2025,3,11), "INV-9001", 36000,  5.0, "131001", "Sonipat",   "Haryana",     CourierNameEnum.dtdc_express,      "AWB-9001", date(2025,3,11), 3, date(2025,3,14), None,           "",           CourierStatusEnum.out_for_delivery),
        ("Sonipat",  "PC-802", "Sonipat Traders",  "9882345678", date(2025,3,13), "INV-9002", 19000,  2.5, "131002", "Sonipat",   "Haryana",     CourierNameEnum.safe_express,      "AWB-9002", date(2025,3,13), 3, date(2025,3,16), None,           "",           CourierStatusEnum.in_transit),

        ("Barwala",  "PC-901", "Barwala Dairy",    "9121234567", date(2025,3,10), "INV-10001",31000,  4.0, "125121", "Barwala",   "Haryana",     CourierNameEnum.jet_line,          "AWB-10001",date(2025,3,11), 4, date(2025,3,15), date(2025,3,15), "",           CourierStatusEnum.delivered),
        ("Barwala",  "PC-902", "Hisar Goods",      "9132345678", date(2025,3,13), "INV-10002",24000,  3.4, "125122", "Barwala",   "Haryana",     CourierNameEnum.bharat_dart,       "AWB-10002",date(2025,3,13), 3, date(2025,3,16), None,           "",           CourierStatusEnum.in_transit),
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
