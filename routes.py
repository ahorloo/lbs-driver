from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pandas as pd
import os, json, calendar
from datetime import datetime, date, timedelta
from collections import defaultdict
from db import get_connection
from config import Config
from mappings import truck_driver_map, truck_number_map
import re
from utils import require_auth




main = Blueprint('main', __name__)

# Inject datetime and calendar globally
@main.app_context_processor
def inject_globals():
    return {
        'now': datetime.now(),
        'calendar': calendar,
    }

# ================================
# ROUTE: Homepage
# ================================
@main.route('/')
def index():
    return render_template('index.html')

# ================================
# ROUTE: Daily Report
# ================================
@main.route('/daily-report')
@require_auth
def daily_report():
    from collections import defaultdict
    grouped_trips = defaultdict(list)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 📅 Get today's trips
        cursor.execute("SELECT * FROM trips WHERE DATE(created_at) = CURDATE()")
        trip_records = cursor.fetchall()

        for trip in trip_records:
            plate_raw = trip.get("device_name") or ""
            plate_clean = plate_raw.replace(" ", "")  # Remove any spaces just in case

            # 🔍 Match partial plate to truck number
            matched_key = next((key for key in truck_number_map if key in plate_clean), None)
            truck_number = truck_number_map.get(matched_key, "Unknown")
            driver_name = truck_driver_map.get(truck_number, "Unknown")

            # 📌 Combine for display: Plate/TruckNumber
            display_name = f"{plate_clean}/{truck_number}"

            # ➕ Add driver/truck info to the trip
            trip["truck_number"] = truck_number
            trip["driver_name"] = driver_name

            grouped_trips[display_name].append(trip)

        return render_template("daily_report.html",
                               devices=grouped_trips,
                               date_start=date.today().strftime('%Y-%m-%d'))

    except Exception as e:
        print("❌ Error loading daily report:", e)
        flash("Error loading today's report. Please try again.", "danger")
        return render_template("daily_report.html",
                               devices={},
                               date_start=date.today().strftime('%Y-%m-%d'))

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


# ================================
# ROUTE: Daily Commentary (Now with field check 🔎)
# ================================
@main.route('/daily_commentary', methods=['GET'])
@require_auth
def daily_commentary():
    from collections import defaultdict

    grouped_trips = defaultdict(lambda: {
        "driver": "Unknown",
        "truck_number": "Unknown",
        "trips": [],
        "total_distance": 0.0,
        "total_fuel": 0.0,
        "trip_count": 0
    })

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 📅 Get today's trips
        cursor.execute("SELECT * FROM trips WHERE DATE(created_at) = CURDATE()")
        trip_records = cursor.fetchall()

        if not trip_records:
            flash("No trips recorded for today", "warning")

        fuel_per_km = 0.3

        for trip in trip_records:
            trip_normalized = {k.lower(): v for k, v in trip.items()}

            plate_raw = trip_normalized.get("device_name", "")
            plate_clean = plate_raw.replace(" ", "")
            matched_key = next((key for key in truck_number_map if key in plate_clean), None)

            truck_number = truck_number_map.get(matched_key, "Unknown")
            driver_name = truck_driver_map.get(truck_number, "Unknown")

            # 📏 Grab route length
            distance = trip_normalized.get("route_length_km") or trip_normalized.get("daily_mileage_km") or 0.0
            try:
                distance = float(distance)
            except (ValueError, TypeError):
                distance = 0.0

            estimated_fuel = round(distance * fuel_per_km, 2)

            # 🧼 Clean start/end locations
            def clean_loc(loc):
                return loc if loc and loc.lower() not in ["unknown", "no", "null"] else "—"

            start_loc = clean_loc(trip_normalized.get("start_location"))
            end_loc = clean_loc(trip_normalized.get("end_location"))

            # 💾 Build grouped data
            grouped_trips[truck_number]["truck_number"] = truck_number
            grouped_trips[truck_number]["driver"] = driver_name
            grouped_trips[truck_number]["trip_count"] += 1
            grouped_trips[truck_number]["total_distance"] += distance
            grouped_trips[truck_number]["total_fuel"] += estimated_fuel

            grouped_trips[truck_number]["trips"].append({
                "start_location": start_loc,
                "end_location": end_loc,
                "route_length_km": distance,
                "estimated_fuel": estimated_fuel
            })

        return render_template(
            "daily_commentary.html",
            grouped_trips=grouped_trips,
            today=date.today().strftime('%Y-%m-%d')
        )

    except Exception as e:
        print("❌ Error loading daily commentary:", e)
        flash("Error loading daily commentary", "danger")
        return render_template("daily_commentary.html", grouped_trips={}, today=date.today().strftime('%Y-%m-%d'))

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# ================================
# ROUTE: Weekly Commentary
# ================================
@main.route('/weekly_commentary', methods=['GET'])
@require_auth
def weekly_commentary():
    from collections import defaultdict

    grouped_trips = defaultdict(lambda: {
        "driver": "Unknown",
        "truck_number": "Unknown",
        "trips": [],
        "total_distance": 0.0,
        "total_fuel": 0.0,
        "trip_count": 0
    })

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 🗓️ Define week range (Monday to Sunday)
        today = date.today()
        week_start = today - timedelta(days=today.weekday())  # Monday
        week_end = week_start + timedelta(days=6)  # Sunday

        cursor.execute("""
            SELECT * FROM trips 
            WHERE DATE(created_at) BETWEEN %s AND %s
        """, (week_start, week_end))
        trip_records = cursor.fetchall()

        if not trip_records:
            flash("No trips recorded for this week", "warning")

        fuel_per_km = 0.3

        for trip in trip_records:
            trip_normalized = {k.lower(): v for k, v in trip.items()}

            plate_raw = trip_normalized.get("device_name", "")
            plate_clean = plate_raw.replace(" ", "")
            matched_key = next((key for key in truck_number_map if key in plate_clean), None)

            truck_number = truck_number_map.get(matched_key, "Unknown")
            driver_name = truck_driver_map.get(truck_number, "Unknown")

            distance = trip_normalized.get("route_length_km") or trip_normalized.get("daily_mileage_km") or 0.0
            try:
                distance = float(distance)
            except (ValueError, TypeError):
                distance = 0.0

            estimated_fuel = round(distance * fuel_per_km, 2)

            def clean_loc(loc):
                return loc if loc and loc.lower() not in ["unknown", "no", "null"] else "—"

            start_loc = clean_loc(trip_normalized.get("start_location"))
            end_loc = clean_loc(trip_normalized.get("end_location"))

            grouped_trips[truck_number]["truck_number"] = truck_number
            grouped_trips[truck_number]["driver"] = driver_name
            grouped_trips[truck_number]["trip_count"] += 1
            grouped_trips[truck_number]["total_distance"] += distance
            grouped_trips[truck_number]["total_fuel"] += estimated_fuel

            grouped_trips[truck_number]["trips"].append({
                "start_location": start_loc,
                "end_location": end_loc,
                "route_length_km": distance,
                "estimated_fuel": estimated_fuel
            })

        return render_template(
            "weekly_commentary.html",
            grouped_trips=grouped_trips,
            week_start=week_start.strftime('%Y-%m-%d'),
            week_end=week_end.strftime('%Y-%m-%d')
        )

    except Exception as e:
        print("❌ Error loading weekly commentary:", e)
        flash("Error loading weekly commentary", "danger")
        return render_template("weekly_commentary.html", grouped_trips={}, week_start="", week_end="")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# ===============================
# Upload New Report
# ===============================
@main.route('/upload', methods=['GET', 'POST'])
@require_auth
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash("⚠️ Please select a file.", "warning")
            return redirect(url_for('main.upload'))

        filename = file.filename
        ext = filename.rsplit('.', 1)[-1].lower()
        if ext not in ['csv', 'json']:
            flash("⚠️ Only CSV or JSON files are allowed.", "warning")
            return redirect(url_for('main.upload'))

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)

        rows = []
        try:
            if ext == 'csv':
                df = pd.read_csv(filepath)
                rows = df.to_dict(orient='records')
            else:
                with open(filepath) as f:
                    data = json.load(f)

                for item in data.get('items', []):
                    # 🔒 Safely access nested keys
                    meta = item.get('meta') or {}
                    device_info = meta.get('device.name')
                    device_name = ''
                    if isinstance(device_info, dict):
                        device_name = device_info.get('value', '')

                    table = item.get('table') or {}
                    for row in table.get('rows', []):
                        row['Device'] = device_name
                        rows.append(row)

            if not rows:
                flash("⚠️ File has no valid trip data.", "warning")
                return redirect(url_for('main.upload'))

            session['rows'] = rows

            # ✅ Gather all unique device names properly
            devices_set = set()
            for row in rows:
                device = str(row.get('Device') or row.get('device_name') or '').strip()
                if device:
                    devices_set.add(device)

            if not devices_set:
                flash("⚠️ No devices found in file.", "warning")
                return redirect(url_for('main.upload'))

            devices = sorted(devices_set)

            return render_template('locations_per_device.html', devices=devices)

        except Exception as e:
            flash(f"❌ Failed to process file: {e}", "danger")
            return redirect(url_for('main.upload'))

    return render_template('upload.html')


# ===============================
# Save Uploaded Trips
# ===============================
@main.route('/save_trips', methods=['POST'])
@require_auth
def save_trips():
    rows = session.get('rows')
    if not rows:
        flash("⚠️ No data found. Please upload again.", "warning")
        return redirect(url_for('main.upload'))

    trip_date_str = request.form.get('trip_date')
    if not trip_date_str:
        flash("⚠️ Please select a trip date.", "warning")
        return redirect(url_for('main.upload'))

    try:
        trip_date = datetime.strptime(trip_date_str, '%Y-%m-%d')
    except ValueError:
        flash("⚠️ Invalid date format.", "warning")
        return redirect(url_for('main.upload'))

    device_locations = {
        dev.replace('_start', ''): (
            request.form.get(f"{dev.replace('_start', '')}_start", '').strip().title(),
            request.form.get(f"{dev.replace('_start', '')}_end", '').strip().title()
        )
        for dev in request.form if dev.endswith('_start')
    }

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            for row in rows:
                device = str(row.get('Device') or row.get('device_name') or '').strip()
                start_location, end_location = device_locations.get(device, ('', ''))

                trip_start = row.get('first_drive_time') or row.get('Trip Start')
                trip_end = row.get('last_drive_time') or row.get('Trip End')

                cursor.execute(
                    '''
                    INSERT INTO trips (
                        device_name, trip_start, trip_end, start_location, end_location,
                        route_length_km, move_duration, stop_duration, stop_count,
                        top_speed_kph, avg_speed_kph, overspeed_count, daily_mileage_km, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''',
                    (
                        device, trip_start, trip_end, start_location, end_location,
                        float(str(row.get('distance', '0')).replace(' Km', '')) if row.get('distance') else 0,
                        row.get('drive_duration') or row.get('Move duration', ''),
                        row.get('stop_duration') or row.get('Stop duration', ''),
                        int(row.get('stop_count', 0) or row.get('Stop count', 0)),
                        int(str(row.get('top_speed', '0')).replace(' kph', '')),
                        int(str(row.get('avg_speed', '0')).replace(' kph', '')),
                        int(row.get('overspeed_count', 0)),
                        float(str(row.get('distance', '0')).replace(' Km', '')),
                        trip_date
                    )
                )
            conn.commit()

        session.pop('rows', None)
        flash("✅ Trips saved successfully!", "success")
        return redirect(url_for('main.dashboard_years'))

    except Exception as e:
        flash(f"❌ Failed to save trips: {e}", "danger")
        return redirect(url_for('main.upload'))


# ===============================
# Dashboard: Years
# ===============================
@main.route('/dashboard')
@require_auth
def dashboard_years():
    years = []
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT DISTINCT YEAR(created_at) AS year
                FROM trips
                ORDER BY year DESC
                '''
            )
            years = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        flash(f"❌ Failed to fetch years: {e}", "danger")

    return render_template('dashboard_years.html', years=years)


# ===============================
# Dashboard: Months
# ===============================
@main.route('/dashboard/<int:year>')
@require_auth
def dashboard_months(year):
    months = []
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT DISTINCT MONTH(created_at) AS month
                FROM trips
                WHERE YEAR(created_at) = %s
                ORDER BY month
                ''', (year,)
            )
            months = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        flash(f"❌ Failed to fetch months: {e}", "danger")

    month_names = {i: calendar.month_name[i] for i in range(1, 13)}

    return render_template(
        'dashboard_months.html',
        year=year,
        months=months,
        month_names=month_names
    )


# ===============================
# Dashboard: Days
# ===============================
@main.route('/dashboard/<int:year>/<int:month>')
@require_auth
def dashboard_days(year, month):
    days = []
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                SELECT DISTINCT DAY(created_at) AS day
                FROM trips
                WHERE YEAR(created_at) = %s AND MONTH(created_at) = %s
                ORDER BY day
                ''', (year, month)
            )
            days = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        flash(f"❌ Failed to fetch days: {e}", "danger")

    return render_template(
        'dashboard_days.html',
        year=year,
        month=month,
        days=days
    )


# ===============================
# Dashboard: Day Trips
# ===============================
@main.route('/dashboard/<int:year>/<int:month>/<int:day>')
@require_auth
def dashboard_day_trips(year, month, day):
    trips_by_device = defaultdict(list)

    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                '''
                SELECT *
                FROM trips
                WHERE YEAR(created_at) = %s AND MONTH(created_at) = %s AND DAY(created_at) = %s
                ''', (year, month, day)
            )
            trips = cursor.fetchall()

            for trip in trips:
                plate = (trip.get("device_name") or "").replace(" ", "")
                matched_key = next((key for key in truck_number_map if key in plate), None)
                truck_number = truck_number_map.get(matched_key, "Unknown")
                driver_name = truck_driver_map.get(truck_number, "Unknown")
                
                # 🛠 No extra 00 here — truck_number is already '007' style
                display_name = f"{plate}/{truck_number}"

                trip["display_name"] = display_name
                trip["truck_number"] = truck_number
                trip["driver_name"] = driver_name

                trips_by_device[display_name].append(trip)

    except Exception as e:
        flash(f"❌ Failed to fetch trips: {e}", "danger")

    return render_template(
        'dashboard_day_trips.html',
        year=year,
        month=month,
        day=day,
        trips_by_device=trips_by_device
    )


# ===============================
# Dashboard: Monthly Summary Per Device
# ===============================
@main.route('/dashboard/<int:year>/<int:month>/summary')
@require_auth
def dashboard_monthly_summary(year, month):
    summaries = defaultdict(lambda: {
        'total_distance': 0,
        'total_overspeeds': 0,
        'total_trips': 0
    })

    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                '''
                SELECT device_name, SUM(route_length_km) AS total_distance,
                       SUM(overspeed_count) AS total_overspeeds, COUNT(*) AS total_trips
                FROM trips
                WHERE YEAR(created_at) = %s AND MONTH(created_at) = %s
                GROUP BY device_name
                ''',
                (year, month)
            )
            rows = cursor.fetchall()
            for row in rows:
                summaries[row['device_name']] = {
                    'total_distance': row['total_distance'],
                    'total_overspeeds': row['total_overspeeds'],
                    'total_trips': row['total_trips']
                }

    except Exception as e:
        flash(f"❌ Failed to fetch monthly summary: {e}", "danger")

    return render_template(
        'dashboard_monthly_summary.html',
        year=year,
        month=month,
        summaries=summaries
    )


# ===============================
# Weekly Summary Per Truck
# ===============================
@main.route('/dashboard/weekly-summary')
@require_auth
def weekly_summary():
    trips_by_week = defaultdict(lambda: defaultdict(list))  # device -> week -> list of trips

    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT device_name, trip_start, trip_end, start_location, end_location, route_length_km
                FROM trips
                ORDER BY device_name, trip_start DESC
            """)
            results = cursor.fetchall()
            for trip in results:
                start_dt = trip['trip_start']
                if not start_dt:
                    continue
                week_key = f"{start_dt.isocalendar()[0]}-W{start_dt.isocalendar()[1]}"
                trips_by_week[trip['device_name']][week_key].append(trip)

    except Exception as e:
        flash(f"❌ Failed to fetch detailed weekly trips: {e}", "danger")

    return render_template('weekly_summary.html', trips_by_week=trips_by_week)


# ===============================
# Monthly Summary Per Truck
# ===============================

@main.route('/dashboard/monthly-summary')
@require_auth
def monthly_summary():
    trips_by_month = defaultdict(lambda: defaultdict(list))  # device -> month -> list of trips

    try:
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT device_name, trip_start, trip_end, start_location, end_location, route_length_km
                FROM trips
                ORDER BY device_name, trip_start DESC
            """)
            results = cursor.fetchall()
            for trip in results:
                start_dt = trip['trip_start']
                if not start_dt:
                    continue
                month_key = f"{start_dt.year}-{start_dt.month:02d}"
                trips_by_month[trip['device_name']][month_key].append(trip)

    except Exception as e:
        flash(f"❌ Failed to fetch detailed monthly trips: {e}", "danger")

    return render_template('monthly_summary.html', trips_by_month=trips_by_month)

# ===============================
# Add New Logbook Entry
# ===============================
@main.route('/logbook-entry', methods=['GET', 'POST'])
@require_auth
def logbook_entry():
    if request.method == 'POST':
        try:
            # 🧠 Grab form inputs and convert empty strings to None for decimals
            def parse_decimal(value):
                return float(value) if value else None

            data = {
                'date': request.form.get('date'),
                'trip_no': request.form.get('trip_no'),
                'consignee': request.form.get('consignee'),
                'terminal': request.form.get('terminal'),
                'destination': request.form.get('destination'),
                'truck_no': request.form.get('truck_no'),
                'pickup_date': request.form.get('pickup_date'),
                'offloading_date': request.form.get('offloading_date'),
                'fuel': parse_decimal(request.form.get('fuel')),
                'road_expense': parse_decimal(request.form.get('road_expense')),
                'toll': parse_decimal(request.form.get('toll')),
                'advance_payment': parse_decimal(request.form.get('advance_payment')),
                'no_of_cont': request.form.get('no_of_cont'),
                'unit_price': parse_decimal(request.form.get('unit_price')),
                'rate': request.form.get('rate'),
                'invoice_date': request.form.get('invoice_date'),
                'payment_rec_date': request.form.get('payment_rec_date'),
                'mode_of_payment': request.form.get('mode_of_payment'),
                'remarks': request.form.get('remarks')
            }

            # ✅ DB connect
            conn = get_connection()
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO daily_logbook (
                    date, trip_no, consignee, terminal, destination, truck_no,
                    pickup_date, offloading_date, fuel, road_expense, toll,
                    advance_payment, no_of_cont, unit_price, rate, invoice_date,
                    payment_rec_date, mode_of_payment, remarks
                ) VALUES (
                    %(date)s, %(trip_no)s, %(consignee)s, %(terminal)s, %(destination)s, %(truck_no)s,
                    %(pickup_date)s, %(offloading_date)s, %(fuel)s, %(road_expense)s, %(toll)s,
                    %(advance_payment)s, %(no_of_cont)s, %(unit_price)s, %(rate)s, %(invoice_date)s,
                    %(payment_rec_date)s, %(mode_of_payment)s, %(remarks)s
                )
            """
            cursor.execute(insert_query, data)
            conn.commit()

            flash('✅ Logbook entry added successfully!', 'success')
            return redirect(url_for('main.logbook_entry'))

        except Exception as e:
            print("❌ Error adding logbook entry:", e)
            flash(f"❌ Something went wrong: {e}", "danger")

            # ❗ Show previous inputs again if there's an error
            return render_template('logbook_entry.html', form_data=request.form)

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return render_template('logbook_entry.html', form_data={})


# ================================
# ROUTE: Finalize Entries
# ================================
@main.route('/finalize-entries')
@require_auth
def finalize_entries():
    from collections import defaultdict

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 📥 Fetch entries from daily_logbook grouped by date
        cursor.execute("SELECT * FROM daily_logbook ORDER BY date DESC")
        entries = cursor.fetchall()

        grouped_entries = defaultdict(list)
        for entry in entries:
            entry_date = entry.get("date", "Unknown")
            grouped_entries[entry_date].append(entry)

        return render_template("finalize_entries.html", grouped_entries=grouped_entries)

    except Exception as e:
        print("❌ Error fetching finalized entries:", e)
        flash("Failed to load finalized entries.", "danger")
        return render_template("finalize_entries.html", grouped_entries={})

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


@main.route('/enter-password', methods=['GET', 'POST'])
def enter_password():
    if request.method == 'POST':
        user_input = request.form.get('password')
        if user_input == Config.ACCESS_PASSWORD:
            session['authenticated'] = True

            # Redirect back to the page they wanted
            next_url = session.pop('next_url', None)
            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for('main.dashboard_month'))  # default landing page
        else:
            flash('Wrong password. Try again!')
    return render_template('password_gate.html')


@main.route('/logout')
def logout():
    session.pop('authenticated', None)
    flash('You’ve been logged out. 👋')
    return redirect(url_for('main.enter_password'))
