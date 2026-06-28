from django import forms


class BaseForm(forms.ModelForm):

    default_class = (
        "w-full px-4 py-2 rounded-lg border mt-1 "
        "border-slate-300 dark:border-slate-600 "
        "bg-slate-50 dark:bg-slate-700 "
        "text-slate-900 dark:text-white "
        "placeholder-slate-400 focus:outline-none "
        "focus:border-transparent transition "
        "[--tw-ring-color:var(--company-color)] focus:ring-2 "
    )

    def apply_style(self):
        for field_name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{self.default_class} {existing}".strip()