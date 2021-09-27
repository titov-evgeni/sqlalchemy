from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Session
from database import Base

session = Session()

association_table1 = Table('association_groups_lessons', Base.metadata,
                           Column('group_id', Integer,
                                  ForeignKey('groups.id')),
                           Column('lesson_id', Integer,
                                  ForeignKey('lessons.id'))
                           )
association_table2 = Table('association_lessons_teachers', Base.metadata,
                           Column('lesson_id', Integer,
                                  ForeignKey('lessons.id')),
                           Column('teacher_id', Integer, ForeignKey(
                               'teacher.id'))
                           )
association_table3 = Table('association_groups_teachers', Base.metadata,
                           Column('group_id', Integer,
                                  ForeignKey('groups.id')),
                           Column('teacher_id', Integer, ForeignKey(
                               'teacher.id'))
                           )


class MixinDataBase:
    __abstract__ = True

    def add_entry(self, *args):
        session.add(self)
        session.commit()
        print(f'Запись: ({self}) была добавлена')

    @classmethod
    def del_entry(cls, entry):
        session.delete(entry)
        session.commit()
        print(f'Запись: ({entry}) была удалена')

    @classmethod
    def update_entry(cls, entry_id: int, *args):
        for arg in args:
            session.query(cls).filter_by(id=entry_id).update(arg)
        session.commit()
        entry = cls.get_entry(entry_id)
        print(f'Запись: ({entry}) была обновлена')

    @classmethod
    def get_entry(cls, entry_id):
        return session.query(cls).get(entry_id)


class Person(MixinDataBase):
    __abstract__ = True

    def __init__(self, full_name: str):
        full_name = full_name.split(' ')
        self.surname = full_name[0]
        self.name = full_name[1]
        self.patronymic = full_name[2]

    def add_entry(self, *args):
        super(Person, self).add_entry(self, *args)

    @classmethod
    def del_entry(cls, entry):
        super(Person, cls).del_entry(entry)

    @classmethod
    def update_entry(cls, person_id: int, *args):
        super(Person, cls).update_entry(person_id, *args)

    @classmethod
    def get_entry(cls, person_id: int):
        return super(Person, cls).get_entry(person_id)

    def __repr__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


class Student(Person, Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    age = Column(Integer)
    group = Column(Integer, ForeignKey('groups.id'))

    def __init__(self, full_name: str, age: int):
        super(Student, self).__init__(full_name)
        self.age = age

    def add_entry(self, group_id: int):
        self.group = group_id
        group = session.query(Group).get(self.group)
        if group:
            super(Student, self).add_entry(self)
        else:
            print("Нет такой группы")

    @classmethod
    def del_entry(cls, student_id: int):
        try:
            student = Student.get_entry(student_id)
            super(Student, cls).del_entry(student)
        except(Exception,):
            print("Нет такого студента")

    @classmethod
    def update_entry(cls, student_id: int, new_surname=None, new_name=None,
                     new_patronymic=None, new_age=None, new_group_id=None):
        student = Student.get_entry(student_id)
        if student:
            lst = []
            if new_name:
                lst.append({"name": new_name})
            if new_surname:
                lst.append({"surname": new_surname})
            if new_patronymic:
                lst.append({"patronymic": new_patronymic})
            if new_age:
                lst.append({"age": new_age})
            if new_group_id:
                lst.append({"group": new_group_id})
            super(Student, cls).update_entry(student_id, *lst)
        else:
            print("Нет такого студента")

    @classmethod
    def get_entry(cls, student_id: int):
        return super(Student, cls).get_entry(student_id)

    def __repr__(self):
        return (f'Студент [{self.id} {self.surname} {self.name} '
                f'{self.patronymic}, Возраст: {self.age}, ID группы:'
                f' {self.group}]')


class Teacher(Person, Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    academic_title = Column(String)

    def __init__(self, full_name: str, academic_title: str):
        super(Teacher, self).__init__(full_name)
        self.academic_title = academic_title

    def add_entry(self, *args):
        super(Teacher, self).add_entry(self)

    @classmethod
    def del_entry(cls, teacher_id: int):
        try:
            teacher = Teacher.get_entry(teacher_id)
            super(Teacher, cls).del_entry(teacher)
        except(Exception,):
            print("Нет такого преподавателя")

    @classmethod
    def update_entry(cls, teacher_id: int, new_surname=None, new_name=None,
                     new_patronymic=None, new_academic_title=None):
        teacher = Teacher.get_entry(teacher_id)
        if teacher:
            lst = []
            if new_name:
                lst.append({"name": new_name})
            if new_surname:
                lst.append({"surname": new_surname})
            if new_patronymic:
                lst.append({"patronymic": new_patronymic})
            if new_academic_title:
                lst.append({"academic_title": new_academic_title})
            super(Teacher, cls).update_entry(teacher_id, *lst)
        else:
            print("Нет такого преподавателя")

    @classmethod
    def get_entry(cls, teacher_id: int):
        return super(Teacher, cls).get_entry(teacher_id)

    def __repr__(self):
        return (f'Преподаватель [{self.id} {self.surname} {self.name} '
                f'{self.patronymic}, {self.academic_title}]')


class Group(MixinDataBase, Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_name = Column(String)
    student = relationship('Student')
    teachers = relationship('Teacher', secondary=association_table3,
                            backref='teacher_group')
    lessons = relationship('Lesson', secondary=association_table1,
                           backref='group_lesson')

    def __init__(self, group_name: str):
        self.group_name = group_name

    def add_entry(self):
        super(Group, self).add_entry(self)

    @classmethod
    def del_entry(cls, group_id: int):
        try:
            group = Group.get_entry(group_id)
            super(Group, cls).del_entry(group)
        except(Exception,):
            print("Нет такой группы")

    @classmethod
    def update_entry(cls, group_id: int, new_group_name=None):
        group = Group.get_entry(group_id)
        if group:
            super(Group, cls).update_entry(group_id,
                                           {"group_name": new_group_name})
        else:
            print("Нет такой группы")

    @classmethod
    def get_entry(cls, group_id: int):
        return super(Group, cls).get_entry(group_id)

    @staticmethod
    def add_lesson_to_group(lesson_id: int, group_id: int):
        try:
            group = Group.get_entry(group_id)
            lesson = Lesson.get_entry(lesson_id)
            group.lessons.append(lesson)
            Group.add_entry(group)
        except(Exception,):
            print("Неправильный идентификатор")

    @staticmethod
    def del_lesson_from_group(lesson_id: int, group_id: int):
        try:
            group = Group.get_entry(group_id)
            lesson = Lesson.get_entry(lesson_id)
            if lesson in group.lessons:
                group.lessons.remove(lesson)
                session.commit()
            else:
                print(f"В группе {group.group_name} нет предмета "
                      f"{lesson.lesson_title}")
        except(Exception,):
            print("Неправильный идентификатор")

    @staticmethod
    def change_lesson_in_group(lesson_id: int, group_id: int,
                               new_lesson_id: int):
        # Group.del_lesson_from_group(lesson_id, group_id)
        # Group.add_lesson_to_group(new_lesson_id, group_id)
        try:
            group = Group.get_entry(group_id)
            lesson = Lesson.get_entry(lesson_id)
            new_lesson = Lesson.get_entry(new_lesson_id)
            for i, item in enumerate(group.lessons):
                if item == lesson:
                    group.lessons[i] = new_lesson
                    session.commit()
                    break
            else:
                print(f"В группе {group.group_name} нет предмета "
                      f"{lesson.lesson_title}")
        except(Exception,):
            print("Неправильный идентификатор")

    @staticmethod
    def add_teacher_to_group(teacher_id: int, group_id: int):
        try:
            group = Group.get_entry(group_id)
            teacher = Teacher.get_entry(teacher_id)
            group.teachers.append(teacher)
            Group.add_entry(group)
        except(Exception,):
            print("Неправильный идентификатор")

    @staticmethod
    def del_teacher_from_group(teacher_id: int, group_id: int):
        try:
            group = Group.get_entry(group_id)
            teacher = Teacher.get_entry(teacher_id)
            if teacher in group.teachers:
                group.teachers.remove(teacher)
                session.commit()
            else:
                print(f"В группе {group.group_name} нет преподавателя "
                      f"{teacher.surname} {teacher.name} {teacher.patronymic}")
        except(Exception,):
            print("Неправильный идентификатор")

    @staticmethod
    def change_teacher_in_group(teacher_id: int, group_id: int,
                                new_teacher_id: int):
        try:
            group = Group.get_entry(group_id)
            teacher = Teacher.get_entry(teacher_id)
            new_teacher = Teacher.get_entry(new_teacher_id)
            for i, item in enumerate(group.teachers):
                if item == teacher:
                    group.teachers[i] = new_teacher
                    session.commit()
                    break
            else:
                print(f"В группе {group.group_name} нет преподавателя "
                      f"{teacher.surname} {teacher.name} {teacher.patronymic}")
        except(Exception,):
            print("Неправильный идентификатор")

    def __repr__(self):
        return f'Группа [ID: {self.id}, Номер: {self.group_name}]'


class Lesson(MixinDataBase, Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    lesson_title = Column(String)
    teachers = relationship('Teacher', secondary=association_table2,
                            backref='teacher_lesson')

    def __init__(self, lesson_title: str):
        self.lesson_title = lesson_title

    def add_entry(self):
        super(Lesson, self).add_entry(self)

    @classmethod
    def del_entry(cls, lesson_id: int):
        try:
            lesson = Lesson.get_entry(lesson_id)
            super(Lesson, cls).del_entry(lesson)
        except(Exception,):
            print("Нет такого предмета")

    @classmethod
    def update_entry(cls, lesson_id: int, new_lesson_title=None):
        lesson = Lesson.get_entry(lesson_id)
        if lesson:
            super(Lesson, cls).update_entry(lesson_id,
                                            {"lesson_title": new_lesson_title})
        else:
            print("Нет такого предмета")

    @classmethod
    def get_entry(cls, lesson_id: int):
        return super(Lesson, cls).get_entry(lesson_id)

    @staticmethod
    def add_teacher_to_lesson(teacher_id: int, lesson_id: int):
        try:
            lesson = Lesson.get_entry(lesson_id)
            teacher = Teacher.get_entry(teacher_id)
            lesson.teachers.append(teacher)
            Lesson.add_entry(lesson)
        except(Exception,):
            print("Неправильный идентификатор")

    @staticmethod
    def del_teacher_from_lesson(teacher_id: int, lesson_id: int):
        try:
            lesson = Lesson.get_entry(lesson_id)
            teacher = Teacher.get_entry(teacher_id)
            if teacher in lesson.teachers:
                lesson.teachers.remove(teacher)
                session.commit()
            else:
                print(f"Предмет {lesson.lesson_title} не ведёт преподаватель "
                      f"{teacher.surname} {teacher.name} {teacher.patronymic}")
        except(Exception,):
            print("Неправильный идентификатор")

    @staticmethod
    def change_teacher_in_lesson(teacher_id: int, lesson_id: int,
                                 new_teacher_id: int):
        try:
            lesson = Lesson.get_entry(lesson_id)
            teacher = Teacher.get_entry(teacher_id)
            new_teacher = Teacher.get_entry(new_teacher_id)
            for i, item in enumerate(lesson.teachers):
                if item == teacher:
                    lesson.teachers[i] = new_teacher
                    session.commit()
                    break
            else:
                print(f"Предмет {lesson.lesson_title} не ведёт преподаватель "
                      f"{teacher.surname} {teacher.name} {teacher.patronymic}")
        except(Exception,):
            print("Неправильный идентификатор")

    def __repr__(self):
        return f'Предмет [ID: {self.id}, Название: {self.lesson_title}]'
