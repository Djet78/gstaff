from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'

    def ready(self):
        from django.db.models.signals import post_delete, pre_save, post_save

        from .models import Article
        from gstaff.signals import handle_files_on_delete, handle_files_on_update, set_instance_cache

        post_delete.connect(handle_files_on_delete, sender=Article, dispatch_uid='article_files_post_delete')

        pre_save.connect(set_instance_cache, sender=Article, dispatch_uid='article_file_path_cache')

        post_save.connect(handle_files_on_update, sender=Article, dispatch_uid='article_files_post_save')
