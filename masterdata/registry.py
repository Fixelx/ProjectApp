MASTERDATA = []


def register_setting(group,name,model,setting_type="table"):

    MASTERDATA.append({
        "group": group,
        "name": name,
        "model": model,
        "model_name": model._meta.model_name,
        "verbose_name": model._meta.verbose_name,
        "verbose_name_plural": model._meta.verbose_name_plural,
        "type": setting_type,
    })