# -*- coding: utf-8 -*-
"""Caliopen user parameters."""

from schematics.models import Model
from schematics.types import (StringType, UUIDType, IntType,
                              DateTimeType, BooleanType)
from schematics.types.compound import ModelType, DictType, ListType
from schematics.transforms import blacklist

from caliopen.base.user.parameters.contact import NewContact, Contact


class NewUser(Model):

    """
    Parameter to create a new user.

    only name and password are required
    a ``NewContact`` can be attached when creating user
    """

    name = StringType(required=True)
    password = StringType(required=True)
    contact = ModelType(NewContact)
    params = DictType(StringType())
    main_user_id = UUIDType()


class User(NewUser):

    """Existing user."""

    user_id = UUIDType(required=True)
    password = StringType()     # not outpout by default, not required
    date_insert = DateTimeType()
    given_name = StringType()
    family_name = StringType()
    contact = ModelType(Contact)

    class Options:
        roles = {'default': blacklist('contact', 'password')}


class Tag(Model):

    """Existing user tag."""

    user_id = UUIDType()
    label = StringType()
    background = StringType()
    color = StringType()

    class Option:
        roles = {'default': blacklist('user_id')}


class NewRule(Model):

    """New filter rule."""

    name = StringType(required=True)
    expr = StringType(required=True)
    position = IntType()
    stop_condition = BooleanType(default=False)
    tags = ListType(StringType)
