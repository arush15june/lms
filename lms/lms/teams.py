import frappe
import requests
from frappe import _

def get_access_token(teams_account):
    settings = frappe.get_doc("LMS Teams Settings", teams_account)
    tenant_id = settings.tenant_id
    client_id = settings.client_id
    client_secret = settings.get_password('client_secret')

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"MS Teams Auth Error: {e}", "MS Teams Integration")
        frappe.throw(_("Failed to authenticate with Microsoft Teams. Check your credentials in LMS Teams Settings."))

def create_teams_meeting(teams_account, subject, start_time, end_time, user_id):
    access_token = get_access_token(teams_account)
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/onlineMeetings"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "startDateTime": start_time,
        "endDateTime": end_time,
        "subject": subject,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            frappe.log_error(f"MS Teams Meeting Creation Error: {response.text}", "MS Teams Integration")
            frappe.throw(
                _("Failed to create Microsoft Teams meeting. Status: {0}, Response: {1}").format(
                    response.status_code, response.text
                )
            )
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"MS Teams API Request Error: {e}", "MS Teams Integration")
        frappe.throw(_("An error occurred while communicating with the Microsoft Teams API."))