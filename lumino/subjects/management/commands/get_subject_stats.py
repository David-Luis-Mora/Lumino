from django.core.management.base import BaseCommand
from django.db import models
from subjects.models import Subject

# class Command(BaseCommand):
#     help = 'Delete all comments for the given post.'
#     def add_arguments(self, parser):
#         parser.add_argument('post_pks', nargs='+', type=int)
#     def handle(self, *args, **options):
#         pass
# for post_pk in options['post_pks']:
#     try:
#         post = Post.objects.get(pk=post_pk)
#     except Post.DoesNotExist:
#         raise CommandError('Post #{post.pk} does not exist')
#     post.comments.delete()
#     self.stdout.write(
#         self.style.SUCCESS('Successfully deleted all comments for post #{post.pk}')
#     )
# shared/management/commands/subject_stats.py


class Command(BaseCommand):
    help = 'Calculates the average grade for each subject.'

    def handle(self, *args, **options):
        for subject in Subject.objects.all():
            enrollments = subject.enrollments.filter(mark__isnull=False)
            if enrollments:
                average = enrollments.aggregate(avg_mark=models.Avg('mark'))['avg_mark']
                self.stdout.write(self.style.SUCCESS(f'{subject.code}: {average:.2f}'))
            else:
                self.stdout.write(self.style.WARNING(f'{subject.code}: No grades available.'))
