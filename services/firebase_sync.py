import requests
import threading
from core.database import get_connection

# Your live Firebase Realtime Database URL
FIREBASE_URL = "https://shda-6245c-default-rtdb.asia-southeast1.firebasedatabase.app"

def sync_data_background():
    """Runs the sync process in the background so the app doesn't freeze."""
    thread = threading.Thread(target=_perform_sync)
    thread.start()

def _perform_sync():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sync New Members to Cloud
    cursor.execute("SELECT id, name, phone, join_date FROM members WHERE sync_status=0")
    for m in cursor.fetchall():
        try:
            resp = requests.post(f"{FIREBASE_URL}/members.json", json={"name": m[1], "phone": m[2], "date": m[3]})
            if resp.status_code == 200:
                cursor.execute("UPDATE members SET sync_status=1 WHERE id=?", (m[0],))
        except: 
            pass # If offline, ignore and try again next time
        
    # Sync New Daan (Donations) to Cloud
    cursor.execute("SELECT id, member_name, amount, date FROM donations WHERE sync_status=0")
    for d in cursor.fetchall():
        try:
            resp = requests.post(f"{FIREBASE_URL}/donations.json", json={"member": d[1], "amount": d[2], "date": d[3]})
            if resp.status_code == 200:
                cursor.execute("UPDATE donations SET sync_status=1 WHERE id=?", (d[0],))
        except: 
            pass

    # Sync Seva & Utsav (Expenses) to Cloud
    cursor.execute("SELECT id, category, name, total_amount, date FROM expenses WHERE sync_status=0")
    for e in cursor.fetchall():
        try:
            resp = requests.post(f"{FIREBASE_URL}/expenses.json", json={"category": e[1], "name": e[2], "amount": e[3], "date": e[4]})
            if resp.status_code == 200:
                cursor.execute("UPDATE expenses SET sync_status=1 WHERE id=?", (e[0],))
        except:
            pass

    conn.commit()
    conn.close()
