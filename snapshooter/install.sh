#!/bin/bash

# install snapshooter


set -o errexit
set -o nounset

#--- variables -----------------------------------------------------
NAME=snapshooter
# source vars
SRC_VERSIONER_SCRIPT=${NAME}-versioner.sh
SRC_DAEMON_SCRIPT=${NAME}-daemon.sh
SRC_SERVICE_SCRIPT=${NAME}-service.sh
SRC_CONF_DEFAULT=${NAME}.conf.default
SRC_MONITOR_FILE_EXAMPLE=etc.ini.example
# install vars
BIN_DIR=/usr/sbin
VERSIONER_BIN=${NAME}-versioner
DAEMON_BIN=${NAME}-daemon
CONF_DIR=/etc/${NAME}
CONF_FILE=${CONF_DIR}/${NAME}.conf
MONITOR_DIR=${CONF_DIR}/monitor.d
MONITOR_FILE=${MONITOR_DIR}/etc.ini
# distribution specific vars
DEBIAN_SERVICE_PATH=/etc/init.d/${NAME}



#--- welcome -------------------------------------------------------
cat <<EOL

snapshooter-fs

== installation ==

EOL



#--- is already installed ? ----------------------------------------
if \
which "${VERSIONER_BIN}" >/dev/null 2>&1 \
|| which "${DAEMON_BIN}" >/dev/null 2>&1 \
|| [ ! -z "`find "${BIN_DIR}" -maxdepth 1 -name "${NAME}*"`" ]
then
	echo "${NAME} seems to already be installed"
	echo
	exit
fi



#--- is user root ? --------------------------------------------------
uid=`id -u`
if [ "${uid}" -ne 0 ]
then
	echo "Error : should be root to run this installation (current uid is ${uid})" >&2
	echo
	exit 1
fi



#--- installation ----------------------------------------------------
# create conf dir
if [ ! -d "${CONF_DIR}" ]
then
	echo "Creating configuration dir : '${CONF_DIR}' ..."
	mkdir -p "${CONF_DIR}"
fi
# create monitor dir
if [ ! -d "${MONITOR_DIR}" ]
then
	echo "Creating monitor dir : '${MONITOR_DIR}' ..."
	mkdir -p "${MONITOR_DIR}"
fi

# get the script dir path (absolute)
scriptdir=`dirname "${0:-}"`
scriptdir=`readlink -f "${scriptdir}"`

# copy the binaries to the bin dir
snapshooter_versioner_bin_path=${BIN_DIR}/${VERSIONER_BIN}
if [ -f "${snapshooter_versioner_bin_path}" ]
then
	echo "Error : the binary '${snapshooter_versioner_bin_path}' already exists"
	echo
	exit 1
else
	echo "Installing versioner binary to '${BIN_DIR}' ..."
	cp -f ${scriptdir}/${SRC_VERSIONER_SCRIPT} "${snapshooter_versioner_bin_path}"
fi
snapshooter_daemon_bin_path=${BIN_DIR}/${DAEMON_BIN}
if [ -f "${snapshooter_daemon_bin_path}" ]
then
	echo "Error : the binary '${snapshooter_daemon_bin_path}' already exists"
	echo
	exit 1
else
	echo "Installing daemon binary to '${BIN_DIR}' ..."
	cp -f ${scriptdir}/${SRC_DAEMON_SCRIPT} "${snapshooter_daemon_bin_path}"
fi

# copy the default configuration
if [ -f "${CONF_FILE}" ]
then
	echo "Error : the configuration file '${CONF_FILE}' already exists"
	echo
	exit 1
else
	echo "Installing default configuration to '${CONF_FILE}' ..."
	cp -f ${scriptdir}/${SRC_CONF_DEFAULT} "${CONF_FILE}"
fi

# copy the default monitor file
if [ -f "${MONITOR_FILE}" ]
then
	echo "Error : the default monitor file '${MONITOR_FILE}' already exists"
	echo
	exit 1
else
	echo "Installing default monitor file to '${MONITOR_FILE}' ..."
	cp -f ${scriptdir}/${SRC_MONITOR_FILE_EXAMPLE} "${MONITOR_FILE}"
fi



#--- messages --------------------------------------------------------
# installation is done
echo
echo "== installation is done =="
echo

# installing service script
cat <<EOL
Should install ${NAME} as a service to automatically starts / stops the daemon when system boots / shutdowns
   For debian user just type the following commands in the shell :
      # sudo cp -f '${SRC_SERVICE_SCRIPT}' '${DEBIAN_SERVICE_PATH}'
      # sudo update-rc.d ${NAME} defaults
      One this is done it can manually starts/stops and check the status of the daemon with :
      # sudo /etc/init.d/${NAME} start
      # sudo /etc/init.d/${NAME} stop
      # sudo /etc/init.d/${NAME} status
   For other users adapt the script named '${SRC_SERVICE_SCRIPT}' to your distribution and configuration your init manager

EOL

# edit configuration file and folder list
cat <<EOL
Should edit the configuration file (${CONF_FILE}) to adjust ${NAME} directories
And also create/edit monitor files (in ${MONITOR_DIR}) to set directories want to monitor for files changes

EOL

# how it works
echo "To see how ${NAME} works, read USE.txt"
echo
