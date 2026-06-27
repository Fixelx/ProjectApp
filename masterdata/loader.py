import importlib

from django.apps import apps


_loaded = False


def autodiscover():

    global _loaded

    if _loaded:
        return

    _loaded = True

    for app in apps.get_app_configs():

        try:
            importlib.import_module(
                f"{app.name}.settings_registry"
            )

        except ModuleNotFoundError:
            pass