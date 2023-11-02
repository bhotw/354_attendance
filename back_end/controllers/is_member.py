from back_end.models import User


def is_member(id, name):
    try:
        user = User.query.filter_by(id=id, name=name).first()

        if user:
            return True
        else:
            return False

    except Exception as e:
        return f"Error: {str(e)}"