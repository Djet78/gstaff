from django.apps import AppConfig


class GamesConfig(AppConfig):
    name = 'games'

    def ready(self):
        from django.db.models.signals import post_delete, pre_save, post_save

        from .models import Game, Platform, Publisher, Studio
        from gstaff.signals import handle_files_on_delete, handle_files_on_update, set_instance_cache

        post_delete.connect(handle_files_on_delete, sender=Game, dispatch_uid='game_files_post_delete')
        post_delete.connect(handle_files_on_delete, sender=Platform, dispatch_uid='platform_files_post_delete')
        post_delete.connect(handle_files_on_delete, sender=Publisher, dispatch_uid='publisher_files_post_delete')
        post_delete.connect(handle_files_on_delete, sender=Studio, dispatch_uid='studio_files_post_delete')

        pre_save.connect(set_instance_cache, sender=Game, dispatch_uid='game_files_path_cache')
        pre_save.connect(set_instance_cache, sender=Platform, dispatch_uid='platform_files_path_cache')
        pre_save.connect(set_instance_cache, sender=Publisher, dispatch_uid='publisher_files_path_cache')
        pre_save.connect(set_instance_cache, sender=Studio, dispatch_uid='studio_files_path_cache')

        post_save.connect(handle_files_on_update, sender=Game, dispatch_uid='game_files_post_save')
        post_save.connect(handle_files_on_update, sender=Platform, dispatch_uid='platform_files_post_save')
        post_save.connect(handle_files_on_update, sender=Publisher, dispatch_uid='publisher_files_post_save')
        post_save.connect(handle_files_on_update, sender=Studio, dispatch_uid='studio_files_post_save')
