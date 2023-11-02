from back_end.models import User, WorkshopHours


def get_info(id, name):
    try:
        user_info = User.query.filter_py(id=id, name=name).first()

        total_hours = WorkshopHours.query.filter_by(id=id).first()

        if user_info and total_hours:
            user_data = {
                'id': user_info.id,
                'name': user_info.name,
                'role': user_info.role,
                'total_hours': total_hours.total_hours
            }
            return user_data
        else:
            return "User information not found."
    except Exception as e:
        return f"Error: {str(e)}"