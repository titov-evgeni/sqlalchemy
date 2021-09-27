from sqlalchemy import and_
from database import DATABASE_NAME, Session
from models import (
    Lesson,
    Student,
    Group,
    Teacher,
    association_table1,
    association_table2,
    association_table3,
)

session = Session()

group = Group("103485")
Group.add_entry(group)
group = Group("256565")
Group.add_entry(group)
group = Group("217-В7856")
Group.add_entry(group)
group = Group("369224")
Group.add_entry(group)

stud = Student("Иванов Николай Викторович", 18)
Student.add_entry(stud, 1)
stud = Student("Петров Евгений Александрович", 20)
Student.add_entry(stud, 3)
stud = Student("Сидоров Антон Алексеевич", 18)
Student.add_entry(stud, 2)
stud = Student("Толкачева Ирина Романовна", 19)
Student.add_entry(stud, 3)

Student.del_entry(2)
Group.del_entry(4)

Student.update_entry(1, new_surname="Киселев", new_group_id=3)
Group.update_entry(2, new_group_name="125-A-789")

lesson = Lesson("Математика")
Lesson.add_entry(lesson)
lesson = Lesson("Физкультура")
Lesson.add_entry(lesson)
lesson = Lesson("Физика")
Lesson.add_entry(lesson)
lesson = Lesson("География")
Lesson.add_entry(lesson)

Group.add_lesson_to_group(1, 2)
Group.add_lesson_to_group(2, 3)
Group.add_lesson_to_group(2, 1)
Group.add_lesson_to_group(3, 2)

Lesson.del_entry(4)

teacher1 = Teacher("Филиппов Иван Борисович", "Доцент")
Teacher.add_entry(teacher1)
teacher2 = Teacher("Крюков Николай Степанович", "Профессор")
Teacher.add_entry(teacher2)
teacher3 = Teacher("Нефедова Екатерина Артёмовна", "Старший преподаватель")
Teacher.add_entry(teacher3)
teacher4 = Teacher("Смирнов Матвей Ярославович", "Старший преподаватель")
Teacher.add_entry(teacher4)

Teacher.del_entry(4)

Group.add_teacher_to_group(3, 2)
Group.add_teacher_to_group(1, 2)
Group.add_teacher_to_group(2, 3)

Lesson.add_teacher_to_lesson(3, 1)
Lesson.add_teacher_to_lesson(2, 2)
Lesson.add_teacher_to_lesson(2, 1)

Group.del_lesson_from_group(1, 2)
Group.change_lesson_in_group(2, 3, 3)

Group.del_teacher_from_group(3, 2)
Group.change_teacher_in_group(1, 2, 3)

Lesson.del_teacher_from_lesson(2, 1)
Lesson.change_teacher_in_lesson(3, 1, 1)

print('*' * 30)
for entry in session.query(Student):
    print(entry)
print('*' * 30)

for entry in session.query(Teacher):
    print(entry)
print('*' * 30)

for entry in session.query(Group):
    print(entry)
print('*' * 30)

for entry in session.query(Lesson):
    print(entry)
print('*' * 30)

for entry in session.query(Student).join(Group).filter(
        Group.group_name == '217-В7856'):
    print(entry)
print('*' * 30)

for entry_group, entry_lesson in session.query(Group, Lesson).filter(
        and_(
            association_table1.c.lesson_id == Lesson.id,
            association_table1.c.group_id == Group.id,
        )):
    print(entry_group, entry_lesson)
print('*' * 30)

for entry_teacher, entry_lesson in session.query(Teacher, Lesson).filter(
        and_(
            association_table2.c.lesson_id == Lesson.id,
            association_table2.c.teacher_id == Teacher.id,
        )):
    print(entry_teacher, entry_lesson)
print('*' * 30)

for entry_group, entry_lesson in session.query(Group, Teacher).filter(
        and_(
            association_table3.c.group_id == Group.id,
            association_table3.c.teacher_id == Teacher.id,
        )):
    print(entry_group, entry_lesson)
print('*' * 30)
