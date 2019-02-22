from django.apps import AppConfig


class GamesConfig(AppConfig):
    name = 'games'

    def ready(self):
        from django.db.models.signals import post_delete, pre_save, post_save

        from .models import Studio, Platform, Game
        from gstaff.signals import handle_files_on_delete, handle_files_on_update, set_instance_cache

        post_delete.connect(handle_files_on_delete, sender=Game, dispatch_uid='game_files_post_delete')
        post_delete.connect(handle_files_on_delete, sender=Platform, dispatch_uid='platform_files_post_delete')
        post_delete.connect(handle_files_on_delete, sender=Studio, dispatch_uid='studio_files_post_delete')

        pre_save.connect(set_instance_cache, sender=Game, dispatch_uid='game_file_path_cache')
        pre_save.connect(set_instance_cache, sender=Platform, dispatch_uid='platform_file_path_cache')
        pre_save.connect(set_instance_cache, sender=Studio, dispatch_uid='studio_file_path_cache')

        post_save.connect(handle_files_on_update, sender=Game, dispatch_uid='game_files_post_update')
        post_save.connect(handle_files_on_update, sender=Platform, dispatch_uid='platform_files_post_update')
        post_save.connect(handle_files_on_update, sender=Studio, dispatch_uid='studio_files_post_update')
