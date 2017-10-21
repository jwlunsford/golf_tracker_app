from peewee import *

db = SqliteDatabase('golfstats.db', pragmas=(('foreign_keys', 'ON')))


def create_tables():
    '''helper function for creating the tables.'''
    db.connect()

    # create tables, only create if they do not exist.
    db.create_tables([Course, Round, Golfer], safe=True)


class BaseModel(Model)::
    class Meta:
        database = db


class Course(BaseModel):
    name = TextField(null=False)
    tee = TextField()
    rating = FloatField(null=False)
    slope = IntegerField(null=False)
    yardage = IntegerField()
    
    class Meta:
        indexes = (
            # create a unique index for course name and tee
            (('name', 'tee'), True)
        )   
        order_by = ('name',)
         

class Round(BaseModel):
    golfer = ForeignKeyField(Golfer)
    course = ForeignKeyField(Course)
    date = DateField(null=False)
    score = IntegerField(null=False)
    putts = IntegerField()
    fairways = IntegerField()
    greens = IntegerField()
    
    class Meta:
        primary_key = CompositeKey('golfer', 'course')
        order_by = ('-date',)


class Golfer(BaseModel):
    name = TextField(null=False)
    dob = DateField()
    handicap = IntegerField(default=0)
    
    
    
    
    
    
    
    