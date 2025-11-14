# emailutils.py
from django.core.mail import EmailMessage
from .pdf_utils import generate_epass_pdf

def send_epass_email(employee):
    pdf_path = generate_epass_pdf(employee)

    subject = "Your Bus Enrollment Form is Accepted"

    body = f"""

Aequs Transport Department

Dear {employee.name},

Your transport enrollment request has been approved.

Please find your Transport e-Pass attached below.
You can download and save this pass for onboarding and future verification.

Regards,
Aequs Transport Team
"""

    email = EmailMessage(
        subject,
        body,
        "techwme19@gmail.com",   # your sending email
        [employee.email],        # employee receiving email
    )

    email.attach_file(pdf_path)
    email.send()
