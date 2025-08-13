# generate_weekly_report.py
import mysql.connector
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from mappings import truck_number_map, truck_driver_map
from config import Config
import sys

# --------- CONFIG ---------
FUEL_PER_KM = 0.33  # liters per km (you can change)
# --------------------------

def detect_date_field(cursor, db, table="trips"):
    """Return one of: 'trip_start', 'trip_date', 'created_at' based on existence."""
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    cols = [r["Field"] for r in cursor.fetchall()]
    for cand in ("trip_start", "trip_date", "created_at"):
        if cand in cols:
            return cand
    # fallback: use first datetime/date-like column
    for c in cols:
        if "date" in c or "time" in c:
            return c
    return None

def fetch_data(start_date, end_date, date_field):
    """Fetch trips from MySQL using the provided date field."""
    conn = mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    query = f"""
        SELECT device_name, start_location, end_location, daily_mileage_km, {date_field}
        FROM trips
        WHERE DATE({date_field}) BETWEEN %s AND %s
        ORDER BY device_name, {date_field}
    """
    cursor.execute(query, (start_date, end_date))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def build_trucks_data(rows, date_field):
    """Group rows by mapped truck id and compute totals."""
    trucks = {}
    for r in rows:
        device = r.get("device_name") or ""
        # extract numeric code (e.g. LBS-GN3634-22 -> 3634)
        parts = device.split('-')
        code_part = ""
        if len(parts) >= 2:
            # prefer the middle part (common pattern) else last numeric chunk
            sec = parts[1]
            code_part = "".join(ch for ch in sec if ch.isdigit())
        if not code_part:
            # try last part
            last = parts[-1]
            code_part = "".join(ch for ch in last if ch.isdigit())
        truck_id = truck_number_map.get(code_part, "UNKNOWN")
        driver = truck_driver_map.get(truck_id, "UNKNOWN")

        if truck_id not in trucks:
            trucks[truck_id] = {"driver": driver, "trips": [], "total_km": 0.0}

        # date formatting
        dt_val = r.get(date_field)
        if isinstance(dt_val, datetime):
            trip_date_str = dt_val.strftime("%Y-%m-%d %H:%M:%S")
        else:
            trip_date_str = str(dt_val)

        dist = r.get("daily_mileage_km") or 0.0
        try:
            dist = float(dist)
        except Exception:
            dist = 0.0

        trucks[truck_id]["trips"].append({
            "date": trip_date_str,
            "start": r.get("start_location") or "",
            "end": r.get("end_location") or "",
            "distance": dist,
            "fuel": round(dist * FUEL_PER_KM, 2)
        })
        trucks[truck_id]["total_km"] += dist

    return trucks

def generate_pdf(trucks_data, start_date, end_date, out_filename):
    """Create PDF with Overview + one page per truck."""
    c = canvas.Canvas(out_filename, pagesize=A4)
    width, height = A4

    # Overview page
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, "WEEKLY TRUCK OPERATIONS SUMMARY")
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, height - 2.7 * cm, f"Company Name: __________________________")
    c.drawString(2 * cm, height - 3.4 * cm, f"Reporting Period: {start_date} – {end_date}")
    c.drawString(2 * cm, height - 4.1 * cm, f"Prepared By: ____________________________")
    c.drawString(2 * cm, height - 4.8 * cm, f"Date Generated: {datetime.now().strftime('%Y-%m-%d')}")

    # Overview metrics
    total_trucks = len(trucks_data)
    total_trips = sum(len(d["trips"]) for d in trucks_data.values())
    total_distance = sum(d["total_km"] for d in trucks_data.values())
    total_fuel = round(total_distance * FUEL_PER_KM, 2)
    total_drivers = len(set(d["driver"] for d in trucks_data.values()))

    # table header
    y = height - 6 * cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y, "Metric")
    c.drawString(10.5 * cm, y, "Value")
    y -= 0.6 * cm
    c.setFont("Helvetica", 10)
    rows = [
        ("Total Trucks Active", str(total_trucks)),
        ("Total Trips Completed", str(total_trips)),
        ("Total Distance Covered (km)", f"{total_distance:.2f}"),
        ("Estimated Fuel Used (Liters)", f"{total_fuel:.2f}"),
        ("Total Drivers Engaged", str(total_drivers)),
    ]
    for label, val in rows:
        c.drawString(2 * cm, y, label)
        c.drawString(10.5 * cm, y, val)
        y -= 0.5 * cm

    c.showPage()

    # Detailed Trip Records: one truck per page
    for truck_id, info in trucks_data.items():
        # Header
        c.setFont("Helvetica-Bold", 13)
        c.drawString(2 * cm, height - 2 * cm, f"Truck: {truck_id}    |    Driver: {info['driver']}")
        c.setFont("Helvetica", 10)
        c.drawString(2 * cm, height - 2.7 * cm, f"Reporting Period: {start_date} – {end_date}")

        # Table header
        y = height - 4.2 * cm
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2 * cm, y, "Trip #")
        c.drawString(4.2 * cm, y, "Start Location")
        c.drawString(9.8 * cm, y, "End Location")
        c.drawString(14.8 * cm, y, "Distance (km)")
        c.drawString(17.4 * cm, y, "Fuel (L)")
        y -= 0.5 * cm
        c.setFont("Helvetica", 10)

        # Trips rows
        for i, t in enumerate(info["trips"], start=1):
            if y < 2.7 * cm:
                c.showPage()
                y = height - 3 * cm
            c.drawString(2 * cm, y, str(i))
            c.drawString(4.2 * cm, y, t["start"][:40])
            c.drawString(9.8 * cm, y, t["end"][:40])
            c.drawRightString(16.8 * cm, y, f"{t['distance']:.2f}")
            c.drawRightString(19.4 * cm, y, f"{t['fuel']:.2f}")
            y -= 0.45 * cm

        # Totals at bottom of truck page
        if y < 4 * cm:
            c.showPage()
            y = height - 3 * cm
        y -= 0.4 * cm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(10 * cm, y, "Total Distance:")
        c.drawRightString(16.8 * cm, y, f"{info['total_km']:.2f}")
        y -= 0.5 * cm
        c.drawString(10 * cm, y, "Estimated Fuel:")
        c.drawRightString(16.8 * cm, y, f"{(info['total_km'] * FUEL_PER_KM):.2f}")

        c.showPage()

    # Insights & Observations page
    # Most frequent start, longest single trip, highest weekly distance
    # compute from trucks_data
    all_trips = []
    for tid, d in trucks_data.items():
        for t in d["trips"]:
            t_copy = dict(t)
            t_copy["truck"] = tid
            all_trips.append(t_copy)

    most_freq_start = "N/A"
    longest_trip_text = "N/A"
    highest_truck_text = "N/A"

    if all_trips:
        from collections import Counter
        start_counts = Counter(t["start"] for t in all_trips)
        most_freq_start = start_counts.most_common(1)[0][0]

        longest = max(all_trips, key=lambda x: x["distance"])
        longest_trip_text = f"{longest['start']} → {longest['end']} ({longest['distance']:.2f} km)"
        highest = max(trucks_data.items(), key=lambda kv: kv[1]["total_km"])
        highest_truck_text = f"Truck {highest[0]} ({highest[1]['total_km']:.2f} km)"

    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 2 * cm, "Insights & Observations")
    c.setFont("Helvetica", 11)
    y = height - 3 * cm
    c.drawString(2 * cm, y, f"- Most frequent start location: {most_freq_start}"); y -= 0.6 * cm
    c.drawString(2 * cm, y, f"- Longest single trip: {longest_trip_text}"); y -= 0.6 * cm
    c.drawString(2 * cm, y, f"- Highest weekly distance: {highest_truck_text}"); y -= 0.6 * cm

    # Notes section
    y -= 0.6 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Notes")
    y -= 0.6 * cm
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, y, "- ")
    c.drawString(2 * cm, y - 0.5 * cm, "- ")
    c.drawString(2 * cm, y - 1.0 * cm, "- ")

    c.showPage()
    c.save()
    print(f"✅ PDF saved as: {out_filename}")

def main():
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()

    # Validate dates briefly
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except Exception:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)

    # connect to detect date field
    conn = mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )
    cur = conn.cursor(dictionary=True)
    date_field = detect_date_field(cur, Config.DB_NAME, table="trips")
    cur.close()
    conn.close()

    if not date_field:
        print("Could not detect a date column in 'trips' table.")
        sys.exit(1)

    rows = fetch_data(start_date, end_date, date_field)
    if not rows:
        print("No trips found for the given date range.")
        sys.exit(0)

    trucks_data = build_trucks_data(rows, date_field)
    out_filename = f"Weekly_Truck_Operations_Summary_{start_date}_to_{end_date}.pdf"
    generate_pdf(trucks_data, start_date, end_date, out_filename)

if __name__ == "__main__":
    main()
