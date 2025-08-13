import os
import sib_api_v3_sdk
from pathlib import Path
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from sib_api_v3_sdk.rest import ApiException

load_dotenv()

templates_path = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


async def send_email(to_email: str, subject: str, html_body: str, plain_body: str = ""):
    """
    Send an email using Brevo (Sendinblue) Transactional Email API.
    """
    sender = {"name": "Billing System", "email": "testfromraj@gmail.com"}
    to = [{"email": to_email}]

    email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_body,
        text_content=plain_body or "Please view HTML email."
    )

    try:
        response = api_instance.send_transac_email(email)
        print(f"Email sent successfully. Response: {response}")
        return response
    except ApiException as e:
        print(f"Error sending email via Brevo: {e}")
        raise


async def send_invoice_email_async(email: str, items, total, paid, change, denominations=None):
    html_body = templates.get_template("invoice.html").render(
        email=email,
        items=items,
        total=total,
        paid=paid,
        change=change,
        denominations=denominations
    )
    plain_body = f"""
    Invoice for {email}.

    Total: {total}
    Paid: {paid}
    Change: {change}

    Balance Denominations:
    {denominations if denominations else 'N/A'}
    """
    await send_email(email, "Your Invoice", html_body, plain_body)

