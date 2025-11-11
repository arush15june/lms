import frappe

def execute():
    # If the new field 'meeting_provider' does not exist, it means an older version is running.
    # This patch is for versions where 'zoom_account' was a simple Link field.
    if not frappe.db.has_column("LMS Live Class", "meeting_provider"):
        return

    # Find all Live Class documents where meeting_provider is not set (i.e., old records)
    # and set it to "LMS Zoom Settings".
    # The data in the 'zoom_account' field is already correct since we didn't rename the field.
    frappe.db.set_value(
        "LMS Live Class",
        {"meeting_provider": ["is", "not set"]},
        "meeting_provider",
        "LMS Zoom Settings",
        update_modified=False,
    )

    frappe.reload_doc("lms", "doctype", "lms_live_class")
    print("Successfully migrated LMS Live Class to support multiple meeting providers.")
