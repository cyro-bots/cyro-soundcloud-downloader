from pathlib import Path

from aiogram.utils.i18n import I18n
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from app.config import settings

from .middlewares.i18n_middleware import CustomI18nMiddleware

locals_dir = Path(__file__).parent.parent / "locales"
locals_dir.mkdir(parents=True, exist_ok=True)


# Create I18n instance (domain should match your .po/.mo files, e.g. 'bot' or 'messages')
i18n = I18n(
    path=locals_dir, default_locale=settings.DEFAULT_LANG, domain="messages"
)
ctx_locale = i18n.ctx_locale

# helpers you can import from this module
gettext = _
lazy_gettext = __

i18n_middleware = CustomI18nMiddleware(i18n)
