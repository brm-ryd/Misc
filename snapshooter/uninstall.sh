#!/bin/bash

set -o errexit
set -o nounset

#--- variables -----------------------------------------------------
NAME=snapshooter
# install vars
BIN_DIR=/usr/sbin
VERSIONER_BIN=${NAME}-versioner
DAEMON_BIN=${NAME}-daemon
CONF_DIR=/etc/${NAME}
CONF_FILE=${CONF_DIR}/${NAME}.conf
# distribution specific vars
DEBIAN_SERVICE_PATH=/etc/init.d/${NAME}



#--- welcome -------------------------------------------------------
cat <<EOL

snapshooter-fs

== uninstallation ==

EOL



#--- is installed ? ------------------------------------------------
if \
! which "${VERSIONER_BIN}" >/dev/null 2>&1 \
&& ! which "${DAEMON_BIN}" >/dev/null 2>&1 \
&& [ -z "`find "${BIN_DIR}" -maxdepth 1 -name "${NAME}*"`" ]
then
	echo "${NAME} seems not to be installed"
	echo
	exit
fi



#--- is user root ? --------------------------------------------------
uid=`id -u`
if [ "${uid}" -ne 0 ]
then
	echo "Error : need root to uninstall (current uid is ${uid})" >&2
	echo
	exit 1
fi



#--- installation ----------------------------------------------------
# removing conf dir
if [ -d "${CONF_DIR}" ]
then
	echo "Removing configuration dir : '${CONF_DIR}' ..."
	rm -fr "${CONF_DIR}"
fi


# removing the binaries from the bin dir
snapshooter_versioner_bin_path=${BIN_DIR}/${VERSIONER_BIN}
if [ -e "${snapshooter_versioner_bin_path}" -o -h "${snapshooter_versioner_bin_path}" ]
then
	echo "Removing versioner binary from '${BIN_DIR}' ..."
	rm -f "${snapshooter_versioner_bin_path}"
fi
snapshooter_daemon_bin_path=${BIN_DIR}/${DAEMON_BIN}
if [ -e "${snapshooter_daemon_bin_path}" -o -h "${snapshooter_daemon_bin_path}" ]
then
	echo "Removing daemon binary to '${BIN_DIR}' ..."
	rm -f "${snapshooter_daemon_bin_path}"
fi



#--- messages --------------------------------------------------------
# uninstallation is done
echo
echo "== uninstallation is done =="
echo

# uninstalling service script
cat <<EOL
You should uninstall ${NAME} service
   For debian user just type the following commands in the shell :
      # sudo /etc/init.d/${NAME} stop
      # sudo rm -f '${DEBIAN_SERVICE_PATH}'
      # sudo update-rc.d ${NAME} remove -f
   For other users remove the service you have eventually build for your distribution and remove it from your init manager
EOL

echo
