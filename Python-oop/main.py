from models import Patient

# Register new patient
patient = Patient(
    first_name="John",
    last_name="Doe",
    date_of_birth="1990-05-15",
    gender="Male",
    contact_number="1234567890"
)
patient.save()

# Retrieve patient
retrieved = Patient.get_by_id(patient.id)
print("Retrieved:", retrieved)

# Update contact
retrieved.update_contact("9876543210")

# Delete record
retrieved.delete()
