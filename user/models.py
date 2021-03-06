from mongoengine import signals

from application import db
from utilities.common import utc_now_ts as now

class User(db.Document):
    username = db.StringField(db_field="u", required=True, unique=True) 
    # db_field is used incase of high traffic app. Reference to username as u, to save lot of characters.
    password = db.StringField(db_field="p", required=True)
    email = db.StringField(db_field="e", required=True, unique=True)
    firstname = db.StringField(db_field='fn', required=True, max_length=50)
    lastname = db.StringField(db_field='ln', required=True, max_length=50)
    created = db.IntField(db_field='c', default=now())
    bio = db.StringField(db_field='b', max_length=160)

    @classmethod # buildin mongoengine method , its always called before object is writen to db
    def pre_save(cls, sender, document, **kwarge):
        document.username = document.username.lower()
        document.email = document.email.lower()

    meta = {                                          # Creating index to make seach quicker
        'indexes': ['username', 'email', '-created']  # -created : Sort Order should be reversed! Most recent created first
    }

signals.pre_save.connect(User.pre_save, sender=User)