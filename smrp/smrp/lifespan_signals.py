from django.dispatch import receiver
from django_asgi_lifespan.signals import asgi_shutdown, asgi_startup
from smrp.db import init_db, close_db

@receiver(asgi_startup)
async def on_startup(sender, **kwargs):
    await init_db()
    
@receiver(asgi_shutdown)
async def on_shutdown(sender, **kwargs):
    await close_db()