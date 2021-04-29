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


class LastLogins(BaseModel):
    timestamp = pw.DateTimeField(null=False)
    srcip = pw.IPField(null=False)
    token = pw.ForeignKeyField(Tokens, backref='lastlogins')
