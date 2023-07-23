from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exam_web_project.accounts'

    def ready(self):
        import exam_web_project.accounts.signals
        result = super().ready()
        return result
