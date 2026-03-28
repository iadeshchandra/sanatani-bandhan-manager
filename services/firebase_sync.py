import requests
import threading
from core.database import get_connection

FIREBASE_URL = "https://your-firebase-project-id.firebaseio.com/" 

def sync_data_background():
    thread = threading.Thread(target=_perform_sync)
    thread.start()

def _perform_sync():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sync Members
    cursor.execute("SELECT id, name, phone, join_date FROM members WHERE sync_status=0")
    for m in cursor.fetchall():
        try:
            resp = requests.post(f"{FIREBASE_URL}/members.json", json={"name": m[1], "phone": m[2], "date": m[3]})
            if resp.status_code == 200:
                cursor.execute("UPDATE members SET sync_status=1 WHERE id=?", (m[0],))
        except: pass
        
    # Sync Donations
    cursor.execute("SELECT id, member_name, amount, date FROM donations WHERE sync_status=0")
    for d in cursor.fetchall():
        try:
            resp = requests.post(f"{FIREBASE_URL}/donations.json", json={"member": d[1], "amount": d[2], "date": d[3]})
            if resp.status_code == 200:
                cursor.execute("UPDATE donations SET sync_status=1 WHERE id=?", (d[0],))
        except: pass

    conn.commit()
    conn.close()

