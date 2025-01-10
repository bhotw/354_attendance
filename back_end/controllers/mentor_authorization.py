from back_end.models import User


def mentor_authorization(reader_id):
    try:
        user = User.query.filter_by(id=reader_id).first()

        if user.role == "mentor" or "Mentor":
            return True
        else:
            return False

    except Exception as e:
        return f"Error: {str(e)}"