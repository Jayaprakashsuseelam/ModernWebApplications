#!/usr/bin/env python3
"""
Script to check database contents and debug the patient display issue
"""

from db import get_connection
from web_app_postgresql import Patient

def check_database():
    """Check database contents directly"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check table structure
        print("🔍 Checking table structure...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'patients' 
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        print("Table structure:")
        for col in columns:
            print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        # Check patient count
        print("\n📊 Checking patient count...")
        cursor.execute('SELECT COUNT(*) FROM patients')
        count = cursor.fetchone()[0]
        print(f"Total patients in database: {count}")
        
        # Get all patients
        print("\n👥 All patients in database:")
        cursor.execute('SELECT * FROM patients ORDER BY id')
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(f"  Row data: {row}")
                print(f"  Length: {len(row)}")
                if len(row) >= 6:
                    print(f"  ID: {row[0]}, Name: {row[1]} {row[2]}, DOB: {row[3]}, Gender: {row[4]}, Contact: {row[5]}")
                else:
                    print(f"  Incomplete row data: {row}")
        else:
            print("  No patients found")
        
        conn.close()
        
        # Test Patient.get_all() method
        print("\n🔍 Testing Patient.get_all() method...")
        try:
            patients = Patient.get_all()
            print(f"Patients returned by Patient.get_all(): {len(patients)}")
            
            for patient in patients:
                print(f"  {patient.to_dict()}")
        except Exception as e:
            print(f"❌ Error in Patient.get_all(): {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_database() 