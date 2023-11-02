from back_end.models import User, db


def get_register(card_id, name, role, email, phone, emergency_contact, emergency_phone, parent_email):

    user = User(
        id=card_id,
        name=name,
        role=role,
        email=email,
        phone_number=phone,
        emergency_contact_name=emergency_contact,
        emergency_contact_phone=emergency_phone,
        parents_email=parent_email
    )

    db.session.add(user)
    db.session.commit()
    return "New Member has been added to the team!!!"

