
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# If you are using a custom user manager
from apps.user.customs.managers import UserManager

class LowercaseEmailField(models.EmailField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.lower() if value else value
class Page(models.Model):
    page_name = models.CharField(
        max_length=100, default="empty", verbose_name="Page Name", unique=True
    )
    description = models.TextField(
        max_length=200, verbose_name="Descriptions", null=True, blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    creation_date = models.DateField(verbose_name="Created At", auto_now_add=True)
    last_updated_date = models.DateField(verbose_name="Last Updated At", auto_now=True)

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self) -> str:
        return str(self.page_name)


class Role(models.Model):
    page = models.ManyToManyField(
        Page, through="RolePageAssignment", verbose_name="Role Page"
    )
    role_name = models.CharField(max_length=100, verbose_name="Role Name")
    description = models.TextField(
        max_length=200, null=True, blank=True, verbose_name="Descriptions"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    creation_date = models.DateField(verbose_name="Created At", auto_now_add=True)
    last_updated_date = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_system_role = models.BooleanField(verbose_name="Is System Role", default=False)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["-id"]

    def __str__(self) -> str:
        return str(self.role_name)
    
        super().delete(*args, **kwargs)

class User(AbstractBaseUser):
    """
    User model
    """

    user_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="User Name"
    )

    email = LowercaseEmailField(max_length=255, unique=True, verbose_name="Email")
    password = models.CharField(max_length=200, verbose_name="Password")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    last_login = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        verbose_name="Last login",
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    is_superuser = models.BooleanField(default=False, verbose_name="Superuser")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    created_user = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="role_created",
    )

    last_updated_user = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_last_updated_user",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "user_role"]

    objects = UserManager()
    
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return str(self.email)

    
    def save(self, *args, **kwargs):
        if not self.role:
            try:
                normal_role = Role.objects.get(role_name='Normal User')
                self.role = normal_role
            except Role.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-id"]




class RolePageAssignment(models.Model):
    page = models.ForeignKey(Page, verbose_name="Page", on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, verbose_name="Role", on_delete=models.CASCADE, null=True, blank=True
    )
    view = models.BooleanField(verbose_name="View", default=True)
    add = models.BooleanField(verbose_name="Add", default=False)
    edit = models.BooleanField(verbose_name="Edit", default=False)
    delete = models.BooleanField(verbose_name="Delete", default=False)

    created_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="role_page_created",
    )

    class Meta:
        verbose_name = "Role Page Assignment"
        verbose_name_plural = "Role Page Assignments"

    def __str__(self) -> str:
        return self.role.role_name + "   <-->   " + self.page.page_name
