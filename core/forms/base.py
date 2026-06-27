from django import forms


class BaseForm(forms.ModelForm):

    default_class = (
        "w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-600 "
        "bg-slate-50 dark:bg-slate-700 text-slate-900 dark:text-white "
        "placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 "
        "focus:border-transparent transition"
    )

    def apply_style(self):
        for field_name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{self.default_class} {existing}".strip()