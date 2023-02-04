from datacenter.models import Schoolkid, Subject, Teacher, Lesson, Chastisement, Commendation, Mark
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
        fix_ediary(full_name, subject)
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько записей! Уточните информацию об ученике!')
    except Subject.DoesNotExist:
        print('Такого предмета нет! Уточните информацию!')
    except Schoolkid.DoesNotExist:
        print('Такого ученика нет! Проверьте введённые данные!')
    except Lesson.DoesNotExist:
        print('Такой урок не найден!')
                

def fix_ediary(full_name, subject):
    
    schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()    
    lesson = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject).order_by('?').first()    
    if lesson:    
        Commendation.objects.create(text=choice(COMMENDATION), created = lesson.date,
                            schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
    else:
        print('Урок не найден')


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

