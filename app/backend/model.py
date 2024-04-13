from datetime import datetime

import peewee as pw

from app.api import init

storage, _, _ = init()


class BaseModel(pw.Model):
    class Meta:
        database = storage.get_db()

    id = pw.AutoField()
    created = pw.DateTimeField(default=datetime.utcnow)


class Tokens(BaseModel):
    value = pw.UUIDField(unique=True)
    expires = pw.DateTimeField(null=True)
    reason = pw.CharField(null=True)  # Can be an external_id


class AccessRequests(BaseModel):
    """
    Scrubbing means an entry was removed from the whitelist chain,
    so access for the user was revoked on that specific IP.
    This is essential to do regularly in order to not poke too many holes in
    the firewall, since users can roam and change IPs a lot.
    The frequency of scrubbing can be determined independently by each sysadmin
    according to their own needs.
    The users are granted access again based on a valid token.
    """

    src_ip = pw.IPField()
    token = pw.ForeignKeyField(Tokens, backref='accessrequests')
    was_scrubbed = pw.BooleanField(default=False)
