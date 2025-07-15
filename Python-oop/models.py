from dataclasses import dataclass
from db import get_connection

@dataclass
class Patient:
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    contact_number: str
    id: int = None

    def save(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO patients (first_name, last_name, date_of_birth, gender, contact_number)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (self.first_name, self.last_name, self.date_of_birth, self.gender, self.contact_number))
                self.id = cur.fetchone()[0]
                print(f"Patient saved with ID: {self.id}")

    @staticmethod
    def get_by_id(patient_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
                row = cur.fetchone()
                if row:
                    return Patient(*row[1:], id=row[0])
                return None

    def update_contact(self, new_contact):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE patients SET contact_number = %s WHERE id = %s", (new_contact, self.id))
                print(f"Contact updated for patient ID {self.id}")

    def delete(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM patients WHERE id = %s", (self.id,))
                print(f"Patient with ID {self.id} deleted")
