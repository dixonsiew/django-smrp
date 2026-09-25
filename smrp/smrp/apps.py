from django.apps import AppConfig


class SmrpConfig(AppConfig):
    name = 'smrp'
    
    def ready(self):
        import smrp.lifespan_signals