from aiogram.utils.i18n import lazy_gettext as _


class Commands:
    START = _(
        """
Hello {fullname}, welcome 🌹

➕ Download easily from SoundCloud with me
🔸 To use, send the link of your SoundCloud song"""
    )

    HELP = "Here is some help text for using the bot."


class Messages:
    SELECT_LANGUAGE = (
        "Please select your language 🇺🇸\n\nلطفا زبان خود را انتخاب کنید 🇮🇷"
    )
    LANGUAGE_CHANGED = _(
        "Your language has been successfully changed 🎉\nPlease restart the bot /start"
    )
    INVALID_URL = _("❌ Please send a valid SoundCloud URL")
    NO_AUDIO_FORMATS = _("❌ No data found for this track")
    DOWNLOAD_ERROR = _("❌ Download failed. Please try again")
