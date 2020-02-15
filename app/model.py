from datetime import datetime

import peewee as pw

from app.db import db


class BaseModel(pw.Model):
    class Meta:
        database = db

    id = pw.AutoField()
    created = pw.DateTimeField(default=datetime.utcnow)


class Tokens(BaseModel):
    value = pw.CharField(unique=True, null=False)
    expires = pw.DateTimeField(null=True)
