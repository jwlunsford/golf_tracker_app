import sqlite3
import optparse
import sys
import datetime
from peewee import *
from collections import OrderedDict
from tabulate import tabulate

# specify DB to connect to
db = SqliteDatabase('golfstats.db')

# PEEWEE MODELS -----------------
def initialize():
    '''database initialization and helper for creating the tables'''
    db.connect()
    # only create if they do not exist.
    db.create_tables([Course, Round, Golfer], True)

class BaseModel(Model):
    class Meta:
        database = db

class Course(BaseModel):
    name = CharField()
    tee = CharField()
    rating = FloatField()
    slope = IntegerField()
    yardage = IntegerField()
    
    class Meta:
        # must add a trailing comma if the tuple of indexes contains only 1 item.
        indexes = (
            (('name','tee'), True), # note the trailing comma
        )     
        order_by = ('name',)     

class Golfer(BaseModel):
    username = CharField(unique=True)
    email = CharField()
    skill = CharField()
    joined = DateTimeField()
    handicap = IntegerField(default=16)
    
    class Meta:
        order_by = ('username',)

class Round(BaseModel):
    # intermediary table relating golfers and courses
    golfer = ForeignKeyField(Golfer)
    course = ForeignKeyField(Course)
    date = DateField()
    score = IntegerField()
    putts = IntegerField()
    fairways = IntegerField()
    greens = IntegerField()



# Course OPERATIONS --------------
def view_courses():
    '''View the courses.'''
    tbl_list = []
    for course in Course.select().order_by(Course.id):
        tbl_list.append([course.id, course.name, course.tee, course.slope, course.rating, course.yardage])
    print "\033[34m"
    print tabulate(tbl_list, headers=["Course ID", "Name", "Tees", "Slope", "Rating", "Yardage"], tablefmt="grid")
    print "\033[30m"
            
def add_course():
    '''Add a course.'''
    choice = raw_input("\nAdd a course? [C]ontinue, [Q]uit: ").lower()
    if choice == 'c':
        name = raw_input('Course name: ')
        tee = raw_input('Tee (color): ')
        yardage = int(raw_input('Tee yardage: '))
        rating = float(raw_input('Rating: '))
        slope = int(raw_input('Slope: '))
    
        # create the instance record
        Course.create(name=name, tee=tee, rating=rating, slope=slope, yardage=yardage)
        print('[+] Course saved.')  
    else:
        return None
        
    
def modify_course():
    '''Modify a course.'''
    try:
        choice = raw_input("\nModify a course? [C]ontinue, [Q]uit: ").lower()
        if choice == 'c':
            tbl_list = []
            for course in Course.select().order_by(Course.id):
                tbl_list.append([course.id, course.name, course.tee])
            print tabulate(tbl_list, headers=["Course ID", "Name", "Tees"], tablefmt="grid")
        
            id = raw_input("\nEnter the course id to select a course: ")
            thiscourse = Course.get(Course.id == id)
            choice = raw_input("What value would you like to change? [N]ame, [T]ee, [R]ating, [S]lope, or [C]ancel: ").lower().strip()
            if choice == 'c':
                return None
            if choice == 'n':
                name = raw_input("Enter a new course name: ")
                thiscourse.name = name
                thiscourse.save()
                print("[!] Course name has been changed to {}.").format(thiscourse.name)
            if choice == 't':
                tee = raw_input("Enter a new tee name: ")
                thiscourse.tee = tee
                thiscourse.save()
                print("[!] Course tee has been changed to {}.").format(thiscourse.tee)
            if choice == 'r':
                rating = raw_input("\nEnter a new rating value: ")
                thiscourse.rating = rating
                thiscourse.save()
                print("[!] Course rating has been changed to {}.").format(thiscourse.rating)
            if choice == 's':
                slope = raw_input("Enter a new slope value: ")
                thiscourse.slope = slope
                thiscourse.save()
                print("[!] Course slope has been changed to {}.").format(thiscourse.slope)
        else:
            return None
    except Exception, e:
        print(e)
            
def select_course():
    try:
        view_courses()
        choice = raw_input("\nTo select a course, enter its ID: ")
        course = Course.get(Course.id == choice)
        print("You selected Course: {} [{}]").format(course.name, course.tee)
        return course
    except:
        print("[X] You've entered an invalid Id.  Please try again.")
        select_course()

    
# Golfer OPERATIONS ----------------    
def add_golfer():
    '''Add a golfer.'''
    try:
        choice = raw_input("\nAdd a golfer? [C]ontinue, [Q]uit: ").lower()
        if choice == 'c':
            with db.transaction():
                user = raw_input('Username: ')
                email = raw_input('Email: ')
                choice = raw_input('Skill level ([B]eginner, [A]mateur, [P]ro): ').lower()
                if choice == 'b':
                    skill = 'Beginner'
                elif choice == 'a':
                    skill = 'Amateur'
                elif choice == 'p':
                    skill = 'Pro'
                else:
                    skill = 'Beginner'
                    joined = datetime.datetime.now()
                    hc = int(raw_input('Handicap (enter 0 if unknown): '))
    
                # create the instance record
                Golfer.create(username=user, email=email, skill=skill, joined=joined, handicap=hc)
                print('[+] Golfer saved.')
        else:
            return None            
    except IntegrityError:
        print('The username is already taken.  Please try again.')
        return addGolfer()
        
    
def modify_golfer():
    '''Modify a golfer.'''
    try:
        choice = raw_input("\nModify a golfer? [C]ontinue, [Q]uit: ").lower()
        if choice == 'c':
            tbl_list = []
            for golfer in Golfer.select().order_by(Golfer.id):
                tbl_list.append([golfer.id, golfer.username, golfer.email, golfer.skill])
            print tabulate(tbl_list, headers=["Golfer", "Username", "Email", "Skill"], tablefmt="grid")
            
            id = raw_input("\nTo modify a golfer, enter their ID: ")
            thisgolfer = Golfer.get(Golfer.id == id)
            choice = raw_input("What value would you like to change? [U]sername, [E]mail, [S]kill, or [C]ancel: ").lower().strip()
            if choice == 'c':
                return None
            if choice == 'u':
                newuser = raw_input("Enter a new username: ")
                thisgolfer.name = newuser
                thisgolfer.save()
                print('Username has been changed to {}').format(thisgolfer.name)
            if choice == 'e':
                newemail = raw_input("Enter a new email address: ")
                thisgolfer.email = newemail
                thisgolfer.save()
                print('Email has been changed to {}').format(thisgolfer.email)
            if choice == 's':
                valid = False
                while valid == False:
                    newskill = raw_input("Enter a new skill level: [B]eginner, [A]mateur, [P]ro: ").lower().strip()
                    if newskill == 'b':
                        thisgolfer.skill = 'Beginner'
                        thisgolfer.save()
                        print("Skill level has been changed to {}").format(thisgolfer.skill)
                        valid = True
                    elif newskill == 'a':
                        thisgolfer.skill = 'Amateur'
                        thisgolfer.save()
                        print("Skill level has been changed to {}").format(thisgolfer.skill)
                        valid = True
                    elif newskill == 'p':
                        thisgolfer.skill = 'Pro'
                        thisgolfer.save()
                        print("Skill level has been changed to {}").format(thisgolfer.skill)
                        valid = True
                    else:
                        print("This is not a valid choice.  Skill level not saved.")
        else:
            return None        
    except Exception, e:
        print(e)
        
    
def view_golfers():
    '''View the golfers.'''
    tbl_list = []
    for golfer in Golfer.select().order_by(Golfer.id):
        tbl_list.append([golfer.id, golfer.username, golfer.skill, golfer.handicap])
    print "\033[34m"
    print tabulate(tbl_list, headers=["Golfer ID:", "Username", "Skill", "Handicap"], tablefmt="grid")
    print "\033[30m"   
        
def select_golfer():
    try:
        view_golfers()
        choice = raw_input("\nTo select a golfer, enter their ID: ")
        golfer = Golfer.get(Golfer.id == choice)
        print("You selected Golfer: {}").format(golfer.username)
        return golfer
    except:
        print("[X] You've entered an invalid id.  Please try again.")
        return None
    

# Round OPERATIONS ---------------
def add_round():
    '''Add a round.'''
    choice = raw_input("\nAdd a round? [C]ontinue, [Q]uit: ").lower()
    if choice == 'c':
        try:
            golfer = select_golfer()
            course = select_course()
            print("You selected {} playing on course, {} [{}].").format(golfer.username, course.name, course.tee)
        
            # enter round details
            date_input = raw_input("Enter the date the round was played.  Please use MM/DD/YYYY format: ")
            date_split = date_input.split("/")
            to_date = datetime.date(int(date_split[2]), int(date_split[0]), int(date_split[1]))
            score = int(raw_input("Enter the score: "))
            putts = int(raw_input("Enter the number of putts: "))
            fairways = int(raw_input("Enter the number of fairways hit: "))
            greens = int(raw_input("Enter the number of greens in regulation: "))
            round = Round.create(
                golfer = golfer,
                course = course,
                date = to_date,
                score = score,
                putts = putts,
                fairways = fairways,
                greens = greens
            )
        except Exception, e:
            print(e)
    else:
        return None     
          
            
    
def modify_round():
    '''Modify a round.'''
    try:
        choice = raw_input("\nModify a round? [C]ontinue, [Q]uit: ").lower()
        if choice == 'c':
            view_rounds()
            round = raw_input("\nTo modify a round, enter its ID: ")
            thisRound = Round.get(Round.id == round)
            choice = raw_input("What value would you like to change? [D]ate, [S]core, [P]utts," + \
                "[G]reens, [F]airways, or [C]ancel: ").lower()
            if choice == 'd':
                newdate = raw_input("Enter a new date in the format DD/MM/YYYY: ")
                date_split = newdate.split("/")
                changedate = datetime.date(int(date_split[2]), int(date_split[0]), int(date_split[1]))
                thisRound.date = changedate
                thisRound.save()
            if choice == 's':
                newscore = int(raw_input("Enter a new score: "))
                thisRound.score = newscore
                thisRound.save()
            if choice == 'p':
                newputts = int(raw_input("Enter number of putts: "))
                thisRound.putts = newputts
                thisRound.save()
            if choice == 'g':
                newgreens = int(raw_input("Enter number of greens: "))
                thisRound.greens = newgreens
                thisRound.save()
            if choice == 'f':
                newfairways = int(raw_input("Enter number of fairways: "))
                thisRound.fairways = newfairways
                thisRound.save()
            if choice == 'c':
                return None 
        else:
            return None
    except Exception, e:
        print("An unexpected error occured.  Try again.")
    
        
def view_rounds():
    '''View the rounds.'''    
    tbl_list = []
    try:
        # select a golfer
        golfer = select_golfer()
        print("\n")
        id = golfer.id
        rounds = (Round
            .select()
            .join(Golfer, JOIN.LEFT_OUTER)
            .where(Golfer.id == id)
            .order_by(Round.date)
        )
        for round in rounds:
            # create a list of values for tabular
            format_date = str.format("{}/{}/{}", round.date.month, round.date.day, round.date.year)
            tbl_list.append([round.id, format_date, round.course.name, round.course.tee, round.score, round.putts, round.fairways, round.greens])
        print "\033[34m"
        print tabulate(tbl_list, headers=["Round", "Date", "Course", "Tee", "Score", "Putts", "Fairways", "Greens"], tablefmt="grid")
        print "\033[30m"
    except Exception, e:
       print("An unexpected error occured.  Try again. ")


def delete_round():
    '''Delete a round.'''
    view_rounds()
    try:
        del_id = int(raw_input("Enter the ID for the round to delete: "))
        thisRound = Round.get(Round.id == del_id)
        with db.transaction():
            thisRound.delete_instance()
    except Exception, e:
        print("An unexpected error occured.")
        print(e)
        
    
    
    
# Calculations -------------------
# Query MANY TO MANY link: http://docs.peewee-orm.com/en/latest/peewee/querying.html#foreign-keys
# DO UNIT TESTING TO MAKE SURE CALCS WORK
def calc_differential(golfer_id):
    '''Calculate the Average Differential from Golf Scores'''
    golfer_rounds = (Round
                    .select()
                    .join(Golfer)
                    .where(Golfer.id == golfer_id)
                    .switch(Round)
                    .join(Course)
                    .order_by(Round.date.desc())
                    .limit(10)
    )
    
    diff = 0
    count = 0
    for rounds in golfer_rounds:
        diff = diff + (rounds.score-rounds.course.rating) * (113/float(rounds.course.slope))
        count += 1
    avg_diff = float(diff) / count
    return avg_diff        
        

def calc_handicap(golfer_id):
    diff = calc_differential(golfer_id)
    hc = round(diff * .96)
    
    # update golfer's handicap
    this_golfer = Golfer.get(Golfer.id == golfer_id)
    this_golfer.handicap = hc
    this_golfer.save()
    
    return hc
    
    
def calc_stats(golfer_id):
    golfer_rounds = (Round
                    .select()
                    .join(Golfer)
                    .where(Golfer.id == golfer_id)
                    .switch(Round)
                    .join(Course)
    )
    
    sum_score = 0
    sum_fairways = 0
    sum_greens = 0
    count_rounds = 0
    for round in golfer_rounds:
        sum_score += round.score
        sum_fairways += round.fairways
        sum_greens += round.greens
        count_rounds += 1
    
    avg_score = sum_score / count_rounds
    avg_fairways = sum_fairways / count_rounds
    pct_fairways = avg_fairways / float(14)
    avg_greens = sum_greens / count_rounds
    pct_greens = avg_greens / float(18)
    
    return avg_score, avg_fairways, avg_greens, pct_fairways, pct_greens
        
    
def view_stats():
    '''View all stats.'''
    
    # select a golfer
    golfer = select_golfer()
    
    # calc the handicap
    hc = calc_handicap(golfer.id)
    print "\033[34m"
    print "\nGolfer's handicap = {}".format(hc)
    
    # calc the averages
    avgScore, avgFairways, avgGreens, pctFairways, pctGreens = calc_stats(golfer.id)
    print "Mean score: {}".format(avgScore)
    print "Mean fairways: {}".format(avgFairways)
    print "Percent fairways: {:.2%}".format(pctFairways)
    print "Mean GIR: {}".format(avgGreens)
    print "Percent GIR: {:.2%}".format(pctGreens)
    print "\033[30m"
    
def menu_loop():
    '''Program loop.'''
    choice = None
    while choice != 'q':
        print('\n*** Golf Main Menu ***')
        for key, value in menu.items():
            print('\t{}) {}').format(key, value.__doc__)
        choice = raw_input('Action: ').lower().strip()
        if choice in menu:
            menu[choice]()
        else:
            print('You entered an invalid choice.  Try again.\n')
            menu_loop()      
                
def exit():
    ''' Exit the program'''
    sys.exit(1)

# create a menu hierarchy for the command line
menu = OrderedDict([
    ('c1', add_course),
    ('c2', modify_course),
    ('c3', view_courses),
    ('g1', add_golfer),
    ('g2', modify_golfer),
    ('g3', view_golfers),
    ('r1', add_round),
    ('r2', modify_round),
    ('r3', view_rounds),
    ('r4', delete_round),
    ('s1', view_stats),
    ('q', exit)
])


def main():
    initialize()
    menu_loop()
    
    
if __name__ == '__main__':
    main()
    
    
            
    