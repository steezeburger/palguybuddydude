from django.contrib.auth.base_user import BaseUserManager

from core.helpers import generate_signup_key


class UserManager(BaseUserManager):
    """
    Manager used for creating users.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # email = self.normalize_email(email)
        if not email:
            raise ValueError('The email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a :class:`User<core.models.User>`
        with the given email and password.

        :param email: :class:`python:str` or :func:`python:unicode`
            Email
        :param password: :class:`python:str` or :func:`python:unicode`
            Password
        :param extra_fields: :class:`python:dict`
            Additional pairs of attribute with value to be set on
            :class:`User<core.models.User>` instance.
        :return: Instance of created :class:`User<core.models.User>`
        :rtype: :class:`core.models.User`
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a :class:`User<core.models.User>`
        with the given email, password and superuser privileges.

        :param email: :class:`python:str`
            Nickname
        :param password: :class:`python:str`
            Password
        :param extra_fields: :class:`python:dict`
            Additional pairs of attribute with value to be set on
            :class:`User<core.models.User>` instance.
        :return: Instance of created :class:`User<core.models.User>`
        :rtype: :class:`core.models.User`
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(email, password, **extra_fields)
