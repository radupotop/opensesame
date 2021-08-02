from datetime import datetime

import peewee as pw

from app.db import db


class BaseModel(pw.Model):
    class Meta:
        database = db

    id = pw.AutoField()
    created = pw.DateTimeField(default=datetime.utcnow)


class Tokens(BaseModel):
    value = pw.UUIDField(unique=True, null=False)
    expires = pw.DateTimeField(null=True)
    description = pw.CharField(null=True)  # Can be an external_id


class AccessRequests(BaseModel):
    timestamp = pw.DateTimeField(null=False)
    src_ip = pw.IPField(null=False)
    token = pw.ForeignKeyField(Tokens, null=False, backref='accessrequests')
