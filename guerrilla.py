from guerrillamail import GuerrillaMailSession
import time


def get_guerrilla_mail(email_name, sender=None):
    if '@' in email_name:
        email_name = email_name.split('@')[0]
    session = GuerrillaMailSession(email_address=email_name)
    content = None

    # count = 0
    while not content:
        # count += 1
        for mail in session.get_email_list():
            if 'guerrilla' not in mail.sender:
                if sender:
                    if sender in mail.sender:
                        content = session.get_email(mail.guid).body
                else:
                    content = session.get_email(mail.guid).body
        time.sleep(5)
    # print(f"Now finished by {count} tries")
    return content

