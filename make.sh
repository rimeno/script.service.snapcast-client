#!/usr/bin/env sh
set -o errexit

readonly PROGNAME=$(basename "$0")
readonly PROGDIR=$(readlink -m "$(dirname "$0")")

NAME=script.service.snapcast-client

if test -z $TMPDIR ; then
    TMPDIR=/tmp/
fi

cd $PROGDIR
VERSION=$(awk -F\" '/^\s*version/ {print $2}' ${PROGDIR}/addon.xml)
OUTPUT=${TMPDIR}/${NAME}-${VERSION}.zip

cd ${PROGDIR}/..
zip --quiet -r $OUTPUT $NAME
echo "→ Addon available at : ${OUTPUT}"
