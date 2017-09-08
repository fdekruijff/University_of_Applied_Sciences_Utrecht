"""
    Title: Practice exercise 4_4
    Author: Floris de Kruijff
    Date created: 08-Sep-17
"""


def new_password(oldpassword: str, newpassword: str) -> bool:
    """
    :param oldpassword: Define old password.
    :param newpassword: Define new password.
    :return: Returns True if new password is good.
    :rtype: bool
    """
    if (oldpassword != new_password) and (len(newpassword) >= 6):
        # Check if new password has at least one digit.
        if any(char.isdigit() for char in newpassword):
            return True
    return False


print(new_password("password", "Password123"))
