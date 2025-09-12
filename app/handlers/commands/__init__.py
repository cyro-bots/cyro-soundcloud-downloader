from aiogram import Router

# Shared router for all command handlers in this package
router = Router()

# Import handlers so they register on import
from . import admin, language, start
