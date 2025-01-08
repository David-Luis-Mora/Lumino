from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Delete all comments for the given post.'

    def add_arguments(self, parser):
        parser.add_argument('post_pks', nargs='+', type=int)

    def handle(self, *args, **options):
        pass
        # for post_pk in options['post_pks']:
        #     try:
        #         post = Post.objects.get(pk=post_pk)
        #     except Post.DoesNotExist:
        #         raise CommandError('Post #{post.pk} does not exist')

        #     post.comments.delete()

        #     self.stdout.write(
        #         self.style.SUCCESS('Successfully deleted all comments for post #{post.pk}')
        #     )
