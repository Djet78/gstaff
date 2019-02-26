from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from django.db.models.signals import post_delete, pre_save, post_save

        from .models import CustomUser
        from gstaff.signals import handle_files_on_delete, handle_files_on_update, set_instance_cache

        post_delete.connect(handle_files_on_delete, sender=CustomUser, dispatch_uid='user_files_post_delete')

        pre_save.connect(set_instance_cache, sender=CustomUser, dispatch_uid='user_files_path_cache')

        post_save.connect(handle_files_on_update, sender=CustomUser, dispatch_uid='user_files_post_save')
