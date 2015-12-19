# -*- coding: utf-8 -*-
"""Caliopen cassandra models related to user."""

from __future__ import absolute_import, print_function, unicode_literals

import logging
import uuid

from cassandra.cqlengine import columns
from elasticsearch import Elasticsearch
from elasticsearch.client.indices import IndicesClient

from caliopen.base.config import Configuration
from caliopen.base.store.model import BaseModel

log = logging.getLogger(__name__)


class UserName(BaseModel):

    """Maintain unicity of user name and permit lookup to user_id."""

    name = columns.Text(primary_key=True)
    user_id = columns.UUID(required=True)


class ReservedName(BaseModel):

    """List of reserved user names."""

    name = columns.Text(primary_key=True)


class User(BaseModel):

    """User main model."""

    user_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(required=True)
    password = columns.Text(required=True)
    date_insert = columns.DateTime()
    given_name = columns.Text()
    family_name = columns.Text()
    params = columns.Map(columns.Text, columns.Text)
    contact_id = columns.UUID()
    main_user_id = columns.UUID()


class Counter(BaseModel):

    """User counters model."""

    user_id = columns.UUID(primary_key=True)
    message_id = columns.Counter()
    thread_id = columns.Counter()
    rule_id = columns.Counter()


class Tag(BaseModel):

    """User tags model."""

    user_id = columns.UUID(primary_key=True)
    label = columns.Text(primary_key=True)
    background = columns.Text()
    color = columns.Text()


class FilterRule(BaseModel):

    """User filter rules model."""

    user_id = columns.UUID(primary_key=True)
    rule_id = columns.Integer(primary_key=True)  # counter.rule_id
    date_insert = columns.DateTime()
    name = columns.Text()
    filter_expr = columns.Text()
    position = columns.Integer()
    stop_condition = columns.Integer(default=None)
    tags = columns.List(columns.Text)


class RemoteIdentity(BaseModel):

    """User remote identities model."""

    user_id = columns.UUID(primary_key=True)
    identity_id = columns.Text(primary_key=True)
    type = columns.Text()
    status = columns.Text()
    credentials = columns.List(columns.Text)
    last_check = columns.DateTime()


class IndexUser(object):

    """User index management class."""

    __url__ = Configuration('global').get('elasticsearch.url')

    @classmethod
    def create(cls, user, **kwargs):
        """Create user index."""
        # Create index for user
        client = Elasticsearch(cls.__url__)
        indice = IndicesClient(client)
        if indice.exists(index=user.user_id):
            if 'delete_existing' in kwargs and kwargs['delete_existing']:
                log.warn('Deleting existing index for user %s' % user.user_id)
                indice.delete(index=user.user_id)
            else:
                log.warn('Index already exists for user %s' % user.user_id)
                return False
        log.info('Creating index for user %s' % user.user_id)
        indice.create(index=user.user_id)
        return True
