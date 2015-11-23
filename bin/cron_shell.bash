#!/bin/bash
set -e

export CASHIER_API_CONFIG=`cat /opt/calolo/cashier/config/config.json`
export PYENV_VERSION=cashier

# restore SHELL env var for cron
SHELL=/bin/bash
# execute the cron command in an actual shell
exec /bin/bash --norc "$@"
