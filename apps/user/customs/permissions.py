from functools import wraps

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import BasePermission

from apps.user.models import Page, RolePageAssignment, User


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


# class CustomPermission(BasePermission):

#     def has_permission(self, request, view):
#         resolver_match = resolve(request.path_info)
#         url_name = resolver_match.url_name.split('-')
#         page_name = url_name[0]
#         get_role = User.objects.filter(email=request.user).values_list('user_role__role_name', flat=True)
#         get_pages = RolePageAssignment.objects.filter(role_id__role_name__in=get_role, is_active=True).values_list('page_id__page_name',
#                                                                                                   flat = True)
#         page_set = set(get_pages)
#         if page_name in page_set:
#             return True
#         else:
#             return False


def get_user_permissions(user: User):
    """
    Retrieve a user's permissions
    """
    if user.is_authenticated:
        role = user.role
        
        if role and role.is_active:
            role_page_assignments = RolePageAssignment.objects.filter(role=role)
            permissions = [
                {
                    "page": assignment.page,
                    "view": assignment.view,
                    "add": assignment.add,
                    "edit": assignment.edit,
                    "delete": assignment.delete,
                }
                for assignment in role_page_assignments
            ]
            print("permissions", permissions)
            return permissions
        else:
            print("User does not have an active role.")
            return []

    raise AuthenticationFailed("User is not authenticated")

class CustomPermissionDenied(APIException):
    status_code = status.HTTP_423_LOCKED
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"


def check_user_has_permissions(
    user: User, required_perm, required_action, required_role=None
):
    user_permissions = get_user_permissions(user)
    if user.role and user.role.role_name == "Super Admin":
        return True

    if isinstance(required_perm, Page):
        required_perm = [required_perm]
        
    # Check user permissions
    for perm in user_permissions:
        if perm["page"] in required_perm:
            if perm[required_action]:
                    return True

    raise CustomPermissionDenied

def custom_permission_required(page_name, action):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            permission = Page.objects.filter(page_name=page_name).first()
            
            print("permission",permission)
            check_user_has_permissions(
                user=request.request.user,
                required_perm=permission,
                required_action=action,
            )
            
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
