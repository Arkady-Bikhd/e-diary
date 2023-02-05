from datacenter.models import Schoolkid, Subject, Lesson, Chastisement, Commendation, Mark
from random import choice
import argparse


COMMENDATION = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем от тебя ожидалось!',
                'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
                'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!',
                'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!'
                'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!',
                'Здорово!']

def main():
    
    try:
        full_name, subject = create_parser()
        schoolkid = get_schoolkid(full_name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject)
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько записей! Уточните информацию об ученике!')
    except Subject.DoesNotExist:
        print('Такого предмета нет! Уточните информацию!')
    except Schoolkid.DoesNotExist:
        print('Такого ученика нет! Проверьте введённые данные!')
    except Lesson.DoesNotExist:
        print('Такой урок не найден!')
                

def get_schoolkid(full_name):

    schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
    return schoolkid


def fix_marks(schoolkid):

    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):

    Chastisement.objects.filter(schoolkid=schoolkid).delete()  


def create_commendation(schoolkid, subject):
 
    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                    subject__title=subject).order_by('?').first()
    if not lesson:    
        print('Урок не найден')
        return
    Commendation.objects.create(text=choice(COMMENDATION), created = lesson.date,
                            schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)


def create_parser():
     
    parser = argparse.ArgumentParser(
        description='Программа исправляет данные в электронном дневнике',
        usage=argparse.SUPPRESS,        
    )
    parser.add_argument('schoolkid', help='Введите фамилию и имя ученика')
    parser.add_argument('subject', help='Введите название предмета')
    try: 
        args = parser.parse_args()
        return args.schoolkid, args.subject
    except SystemExit:
        parser.print_help()
        raise


if __name__ == "__main__":

    main()

