# -*- coding: utf-8 -*-
"""Caliopen models related to contact definition."""
from __future__ import absolute_import, print_function, unicode_literals
from datetime import datetime
import uuid

from cassandra.cqlengine import columns
from caliopen.base.store.model import BaseModel, BaseIndexDocument
from caliopen.base.store.mixin import IndexTagMixin


class BaseContactModel(BaseModel):

    """Base class for contact related models."""

    user_id = columns.UUID(primary_key=True)
    contact_id = columns.UUID(primary_key=True)     # clustering key
    date_insert = columns.DateTime(default=datetime.utcnow())
    date_update = columns.DateTime()


class Contact(BaseContactModel):

    """Contact model."""

    # Redefine, need default
    deleted = columns.Integer(default=0)
    title = columns.Text()          # computed value, read only
    # detailed name structure
    given_name = columns.Text()
    additional_name = columns.Text()
    family_name = columns.Text()
    name_prefix = columns.Text()
    name_suffix = columns.Text()
    tags = columns.List(columns.Text)
    groups = columns.List(columns.Text)
    # everything else in a map
    infos = columns.Map(columns.Text, columns.Text)


class Organization(BaseContactModel):

    """Contact organizations model."""

    organization_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    deleted = columns.Integer(default=0)
    label = columns.Text()
    department = columns.Text()
    job_description = columns.Text()
    name = columns.Text()
    title = columns.Text()
    is_primary = columns.Integer(default=0)
    type = columns.Text()   # work, other


class PostalAddress(BaseContactModel):

    """Contact postal addresses model."""

    address_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    label = columns.Text()
    type = columns.Text()
    is_primary = columns.Integer(default=0)
    street = columns.Text()
    city = columns.Text()
    postal_code = columns.Text()
    country = columns.Text()
    region = columns.Text()


class Email(BaseContactModel):

    """Contact emails model."""

    address = columns.Text(primary_key=True)
    label = columns.Text()
    is_primary = columns.Integer(default=0)
    type = columns.Text()   # home, work, other


class IM(BaseContactModel):

    """Contact instant messaging adresses model."""

    address = columns.Text(primary_key=True)
    label = columns.Text()
    type = columns.Text()
    protocol = columns.Text()
    is_primary = columns.Integer(default=0)


class Phone(BaseContactModel):

    """Contact phones model."""

    number = columns.Text(primary_key=True)
    type = columns.Text()
    is_primary = columns.Integer(default=0)
    uri = columns.Text()    # RFC3966


class SocialIdentity(BaseContactModel):

    """Any contact social identity (facebook, twitter, linkedin, etc)."""

    name = columns.Text(primary_key=True)
    type = columns.Text()
    # Abstract everything else in a map
    infos = columns.Map(columns.Text, columns.Text)


class PublicKey(BaseContactModel):

    """Contact public cryptographic keys model."""

    name = columns.Text(primary_key=True)
    type = columns.Text()
    size = columns.Integer()
    key = columns.Text()
    expire_date = columns.DateTime()
    fingerprint = columns.Text()


class Lookup(BaseModel):

    """Lookup any information needed to recognize a user contact."""

    user_id = columns.UUID(primary_key=True)
    value = columns.Text(primary_key=True)
    contact_id = columns.UUID()
    type = columns.Text()
    lookup_id = columns.Text()


class IndexedContact(BaseIndexDocument, IndexTagMixin):

    """Indexed contact with helpers methods."""

    columns = ['contact_id', 'title', 'given_name', 'additional_name',
               'family_name', 'name_suffix', 'name_prefix',
               'organizations', 'postal_addresses', 'emails', 'ims',
               'phones', 'social_identities', 'public_keys', 'labels',
               'groups', 'infos']

    doc_type = 'contacts'
