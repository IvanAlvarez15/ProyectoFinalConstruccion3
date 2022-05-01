from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, first_name, last_name, country, birthday, email, gender, phone, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The username must be set'))
        if not first_name:
            raise ValueError(_('The first_name must be set'))
        if not last_name:
            raise ValueError(_('The lastname must be set'))
        if not country:
            raise ValueError(_('The country must be set'))
        if not email:
            raise ValueError(_('The email must be set'))
        if not birthday:
            raise ValueError(_('The birthday must be set'))
        if not gender:
            raise ValueError(_('The gender must be set'))
        if not phone:
            raise ValueError(_('The phone number must be set'))

        email = self.normalize_email(email)
        user = self.model(
                username=username,
                first_name=first_name,
                last_name=last_name,
                country=country,
                birthday=birthday,
                email=email,
                gender=gender,
                phone=phone, **extra_fields)

        user.set_password(password)
        user.check_unity = user.hash_unity_password(password)
        user.save()
        return user


    def create_superuser(self, username, first_name, last_name, country, birthday, email, gender, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, first_name, last_name, country, birthday, email, gender, phone, password, **extra_fields)
