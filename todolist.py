from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_tasks(date=None, missed=False):
    if date is None and not missed:
        rows = session.query(Table).all()
    elif missed:
        rows = session.query(Table).filter(Table.deadline < date).all()
    else:
        rows = session.query(Table).filter(Table.deadline == date).all()
    return rows


def add_task():
    print('Enter task')
    task = input()
    print('Enter deadline')
    deadline = datetime.strptime(input(), '%Y-%m-%d')
    new_row = Table(task=task, deadline=deadline)

    session.add(new_row)
    session.commit()
    print('The task has been added!')


def print_tasks(rows, str_):
    if len(rows) == 0:
        print('Nothing to do!')
    temp.clear()
    for i, row in enumerate(rows):
        temp[str(i + 1)] = row.id
        print(str_.format(i + 1, row.task, datetime.strftime(row.deadline, frm_day)))
    print()


def print_tasks_today():
    print('Today {}:'.format(datetime.strftime(today, frm_day)))
    print_tasks(get_tasks(today), '{0}. {1}')


def print_tasks_week():
    for d in range(7):
        day = today + timedelta(days=d)
        print(datetime.strftime(day, '%A %d %b:'))
        print_tasks(get_tasks(), '{0}. {1}')


def close():
    print("\nBye!")
    exit()


def print_tasks_all():
    count = 1
    tasks = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    for task_x in tasks:
        print("{0}. {1}. {2} {3}".format(count, task_x, task_x.deadline.day, task_x.deadline.strftime('%b')))


def print_missed_tasks():
    print('All tasks:')
    print_tasks(get_tasks(), '{0}. {1}. {2}')


def delete_task():
    print('Chose the number of the task you want to delete:')
    print_tasks(get_tasks(), '{0}. {1}. {2}')
    delete = input()
    session.query(Table).filter(Table.id == temp[delete]).delete()
    session.commit()
    print('The task has been deleted!')


today = datetime.today()
frm_day = '%d %b'
temp = dict()
while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
""")
    menu = input()
    if menu == "0":
        close()
    elif menu == "1":
        print_tasks_today()
    elif menu == "2":
        print_tasks_week()
    elif menu == "3":
        print_tasks_all()
    elif menu == "4":
        print_missed_tasks()
    elif menu == "5":
        add_task()
    elif menu == "6":
        delete_task()
