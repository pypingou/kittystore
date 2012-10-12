# -*- coding: utf-8 -*-

"""
Copyright (C) 2012 Aurelien Bompard <abompard@fedoraproject.org>
Author: Aurelien Bompard <abompard@fedoraproject.org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.
See http://www.gnu.org/copyleft/gpl.html  for the full text of the
license.
"""

import datetime

from zope.interface import implements
from storm.locals import *
from mailman.interfaces.messages import IMessage

from kittystore.utils import get_message_id_hash
from .hack_datetime import DateTime

# pylint: disable-msg=R0902,R0913,R0903
# R0902: Too many instance attributes (X/7)
# R0913: Too many arguments (X/5)
# R0903: Too few public methods (X/2)


__all__ = ("List", "Email", "Attachment")


class List(object):
    # The 'List' name is part of storm's locals
    # pylint: disable-msg=E0102
    """
    An archived mailing-list.

    Not strictly necessary yet since the list name is used in the email table,
    but at some point we'll want to store more information on lists in the
    database.
    """

    __storm_table__ = "list"

    name = Unicode(primary=True)
    display_name = Unicode()

    def __init__(self, name):
        self.name = unicode(name)


class Email(object):
    """
    An archived email, from a mailing-list. It is identified by both the list
    name and the message id.
    """

    implements(IMessage)
    __storm_table__ = "email"
    __storm_primary__ = "list_name", "message_id"

    list_name = Unicode()
    message_id = Unicode()
    sender_name = Unicode()
    sender_email = Unicode()
    subject = Unicode()
    content = Unicode()
    date = DateTime()
    in_reply_to = Unicode()
    message_id_hash = Unicode()
    thread_id = Unicode()
    full = RawStr()
    archived_date = DateTime(default_factory=datetime.datetime.now)
    # path is required by IMessage, but it makes no sense here
    path = None

    def __init__(self, list_name, message_id):
        self.list_name = unicode(list_name)
        self.message_id = unicode(message_id)
        self.message_id_hash = unicode(get_message_id_hash(self.message_id))


class Attachment(object):

    __storm_table__ = "attachment"
    __storm_primary__ = "list_name", "message_id", "counter"

    list_name = Unicode()
    message_id = Unicode()
    counter = Int()
    name = Unicode()
    content_type = Unicode()
    encoding = Unicode()
    size = Int()
    content = RawStr()


# References

Email.attachments = ReferenceSet(
        (Email.list_name,
         Email.message_id),
        (Attachment.list_name,
         Attachment.message_id),
        )
