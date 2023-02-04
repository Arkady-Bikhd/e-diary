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
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject)
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько записей! Уточните информацию об ученике!')
    except Subject.DoesNotExist:
        print('Такого предмета нет! Уточните информацию!')
    except Schoolkid.DoesNotExist:
        print('Такого ученика нет! Проверьте введённые данные!')


def fix_marks(schoolkid):
    
    marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
	
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject):
    
    commendation = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем от тебя ожидалось!',
                'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
                'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!',
                'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!'
                'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!',
                'Здорово!']    
    lesson = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject).order_by('?').first()    
    Commendation.objects.create(text=choice(commendation), created = lesson.date,
                            schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)


def check_input_args(input_argument):

    if not input_argument:
        raise argparse.ArgumentTypeError(
            'Не введено значение аргумента!'
        )
    return input_argument


def create_parser():
     
    parser = argparse.ArgumentParser(
        description='Программа исправляет данные в электронном дневнике',
    )
    parser.add_argument('schoolkid', type=check_input_args, help='Введите фамилию и имя ученика')
    parser.add_argument('subject', type=check_input_args, help='Введите название предмета')
    args = parser.parse_args()
    return args.schoolkid, args.subject


if __name__ == "__main__":

    main()

