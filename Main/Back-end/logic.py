"""
DEVELOPER: Ammar Osmun, Tommy Ngo
TASK: Sprint 2
Backend Logic for Employment Verification. Handles validation and processing of form data.

"""

def validate_verification(data):
    """
    Check if all required fields are filled out.
    - Make sure nothing is empty
    - Make sure hours per week is a number
    - Make sure a document is uploaded
    Return True or False.
    """

    # TODO: Add validation rules here
    return True


def process_submission(data):
    """
    Main function to handle submission.
    - Call validate_verification()
    - If valid, send data to storage.py
    - Return success or error message
    """

    # TODO: Connect to storage.save_verification()
    return True, "Submitted successfully."
