from django.contrib.auth.models import BaseUserManager
import datetime

class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            user_role=None,
            password=None,
            user_name=None,
            *args,
            **kwargs,
    ):
        if not email:
            raise ValueError("User must have an email address")
        if super().get_queryset().filter(email=self.normalize_email(email)):
            raise ValueError("User with this email address already exists")
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            last_login=datetime.datetime.now(),
            user_name=user_name
        )
        user.set_password(password)
        user.save(using=self._db)
        # user_role = user_role if user_role else []
        # for i in user_role:
        #     user.user_role.add(i)

        return user

    def create_superuser(
            self,
            email,
            password=None,
            user_role=[14],
    ):
        user = self.create_user(
            email, password=password, user_role=user_role
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        return self.model.objects.create_user(**kwargs)
