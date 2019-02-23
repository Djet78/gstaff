import os


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#              File Deleting Signals
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def _field_path_gen(sender, instance):
    """ Yields tuples: ('file_field_name', 'file_path')

    All data is associated with given sender and instance objects
    Yields only fields specified in instance.FILE_FIELDS attr
    """
    for file_field in sender.FILE_FIELDS:
        file = getattr(instance, file_field)
        if file.name:  # prevent fails when file wasn't specified for old instance
            yield (file_field, file.path)


def _delete_files(file_pathways):
    for path in file_pathways:
        if os.path.isfile(path):
            os.remove(path)
        else:
            # TODO think about handling absent files (may be logging)
            pass


def handle_files_on_delete(sender, instance, **kwargs):
    """ Delete model instance files from filesystem when instance is deleted.

    Model file fields to delete, should be specified in
    'FILE_FIELDS' (list or tuple) Model attr.

    :raise AttributeError: if Model haven't field specified in Model.FILE_FIELDS attr.
    """
    deletables = (path for _, path in _field_path_gen(sender, instance))
    _delete_files(deletables)


def set_instance_cache(sender, instance, **kwargs):
    """ Adds 'files_cache' dict: {'file_field_name': 'old_path', ..., } to instance """
    old_instance = sender.objects.filter(pk=instance.pk).first()
    if old_instance is not None:
        instance.files_cache = {
            field: path for field, path in _field_path_gen(sender, old_instance)
        }


def handle_files_on_update(sender, instance, **kwargs):
    """ Delete model instance files from filesystem when instance is updated.

    Model file fields to delete, should be specified in
    'FILE_FIELDS' (list or tuple) Model attr.

    :raise AttributeError: if Model haven't field specified in Model.FILE_FIELDS attr.
    """
    if hasattr(instance, 'files_cache') and instance.files_cache:
        deletables = []
        for field, new_path in _field_path_gen(sender, instance):
            old_path = instance.files_cache[field]
            if old_path != new_path:
                deletables.append(old_path)

        if deletables:
            _delete_files(deletables)
