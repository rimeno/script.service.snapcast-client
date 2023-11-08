#!/usr/bin/env sh
set -o errexit

PROGDIR=$(readlink -m "$(dirname "$0")")
readonly PROGDIR

NAME=script.service.snapcast-client

if test -z "$TMPDIR" ; then
    TMPDIR=/tmp/
fi

cd "$PROGDIR"
VERSION="$(awk -F\" '/^\s*version/ {print $2}' "${PROGDIR}/addon.xml")"
OUTPUT="${TMPDIR}/${NAME}-${VERSION}.zip"

cd "${PROGDIR}/.."
zip --quiet -r "$OUTPUT" "$NAME" --exclude '*.git*'
echo "→ Addon available at : ${OUTPUT}"
