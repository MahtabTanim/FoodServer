def detectUser(user):
    if user.role == 1:
        return "restaurantDashboard"

    if user.role == 2:
        return "custDashboard"

    if user.role == None and user.is_superadmin:
        return "/admin"
