#!/bin/sh
set -e

DOMAIN="messages"
LOCALES_DIR="locales"

# 1. Extract strings → messages.pot
extract() {
  echo "🔄 Extracting messages into $DOMAIN.pot..."
  pybabel extract -F babel.cfg -o $LOCALES_DIR\/$DOMAIN.pot ./app
}

# 2. Init new language
init() {
  lang=$1
  echo "🌍 Initializing $lang..."
  pybabel init -i $LOCALES_DIR\/$DOMAIN.pot -d $LOCALES_DIR -D $DOMAIN -l $lang
}

# 3. Update existing translations
update() {
  echo "🔄 Updating translations..."
  pybabel update -i $LOCALES_DIR\/$DOMAIN.pot -d $LOCALES_DIR -D $DOMAIN
}

# 4. Compile to .mo
compile() {
  echo "⚡ Compiling translations..."
  pybabel compile -d $LOCALES_DIR -D $DOMAIN
}

# CLI dispatcher
case "$1" in
  extract) extract ;;
  init) init $2 ;;
  update) update ;;
  compile) compile ;;
  all)
    extract
    update
    compile
    ;;
  *)
    echo "Usage: $0 {extract|init <lang>|update|compile|all}"
    exit 1
    ;;
esac
