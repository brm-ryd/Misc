#!/bin/sh

set -o errexit
set -o nounset

#--- variables -----------------------------------------------------
NAME=snapshooter
CONF_DIR=/etc/${NAME}
CONF_FILE=${CONF_DIR}/${NAME}.conf



#-- checks the user is root ----------------------------------------
uid=`id -u`
if [ "${uid}" -ne 0 ]
then
	echo "Error : need root to run this daemon (current uid is ${uid})" >&2
	exit 1
fi



#--- configuration -------------------------------------------------
# configuration
if [ -f "${CONF_FILE}" ]
then
	. "${CONF_FILE}"
fi



#--- get parameters from configuration -----------------------------
# folders
monitor_dir=${MONITOR_DIR:-${CONF_DIR}/monitor.d}
log_dir=${LOG_DIR:-/var/log/${NAME}}
datas_dir=${DATAS_DIR:-/var/${NAME}}
backup_dir=${BACKUP_DIR:-${datas_dir}/backups}
# files
pid_file=${PID_FILE:-/var/run/${NAME}.pid}
process_file=${PROCESS_FILE:-${datas_dir}/process.tmp}
# binaries
snapshooter_versioner_bin=${SNAPSHOOTER_VERSIONER_BIN:-/usr/sbin/${NAME}-versioner}



#--- check / create folders and files ------------------------------
# monitor dir
if [ ! -d "${monitor_dir}" ]
then
	mkdir -p "${monitor_dir}"
fi
# log dir
if [ ! -d "${log_dir}" ]
then
	mkdir -p "${log_dir}"
fi
# datas dir
if [ ! -d "${datas_dir}" ]
then
	mkdir -p "${datas_dir}"
fi
# backup dir
if [ ! -d "${backup_dir}" ]
then
	mkdir -p "${backup_dir}"
fi
# process file
if [ ! -f "${process_file}" ]
then
	touch "${process_file}"
fi



#-- create pid file or exit ----------------------------------------
# if pid file doesn't exist
if [ ! -f "${pid_file}" ]
then
	# we create it, storing the current pid
	echo $$ > "${pid_file}"
# a pid file already exist
else
	# it means that an other instance of this daemon is runing
	# so we advertise the user and exit
	echo "Error : An other instance of this daemon is already runing (with pid $(cat "${pid_file}"))"
	exit 1
fi



#--- log file ------------------------------------------------------
#log_file=${log_dir}/daemon.log.`date '+%Y-%m-%d'`
log_file=${log_dir}/daemon.log
echo "Log to : ${log_file}"
# if the log file doesn't exist
if [ ! -f "${log_file}" ]
then
	# we create it
	echo "${NAME}-daemon log file" > "${log_file}"
	echo "#=========================================================" >> "${log_file}"
fi
echo >> "${log_file}"
echo "#------------------------------ `date '+%Y-%m-%d %Hh%Mm%Ss'` ------------------------------" >> "${log_file}"
echo >> "${log_file}"



#--- functions -----------------------------------------------------
# return the list of the configuration files of folders (find in ${monitor_dir})
getMonitorFileList() {
	find "${monitor_dir}" -maxdepth 1 -type f -iname "*.ini"
}
# exit cleanly
cleanExit() {
	children=${1:-}

	# removing pid file (if exists)
	if [ -f "${pid_file}" ]
	then
		echo "Removing pid file ..." >> "${log_file}"
		rm -f "${pid_file}"
	fi

	echo "Killing children ..." >> "${log_file}"
	# loop each its children pid
	for p in ${children}
	do
		# send terminate signal to child
		if ps --pid ${p} -o pid,ppid |grep -E "^[[:space:]]*${p}[[:space:]]+$$[[:space:]]*$" >/dev/null 2>&1
		then
			echo "Sending term signal to child with PID ${p} ..." >> "${log_file}"
			kill ${p} || continue
			# sleep a little
			sleep 0.2
		fi
	done

	echo "Exiting" >> "${log_file}"
	exit
}



#--- run -----------------------------------------------------------
# trap an exit event
trap "
	trap '' INT TERM
	echo '[`date '+%Hh%Mm%Ss'`] Traped EXIT signal ...' >> '${log_file}'
	cleanExit ''
" EXIT
# number of monitored folders
number_of_monitored_folders=0
# list of the children pid
children_pid=''
# for each monitor file
IFS="
"
for m in `getMonitorFileList`
do
	IFS=" "
	#echo "Using configuration file : ${m} ..." >> "${log_file}"
	# folder configuration file exists
	if [ -f "${m}" ]
	then
		# -- get the infos
		f_path=`grep "^path=" "${m}" 	|awk -F '=' '{print $2}'`
		delay=`grep "^delay=" "${m}" 	|awk -F '=' '{print $2}'`
		depth=`grep "^depth=" "${m}" 	|awk -F '=' '{print $2}'`

		# -- check infos
		# path must exists
		if [ ! -d "${f_path}" ]
		then
			echo "Error : the folder path specified '${f_path}' doesn't" >> "${log_file}"
			exit 1
		fi
		# delay must be an integer which minimum is 5
		if ! echo -n "${delay}" |grep -E "^([5-9]|[1-9][0-9]+)$" >/dev/null 2>&1
		then
			echo "Error : the delay value '${delay}' is not valid" >> "${log_file}"
			exit 1
		fi
		# depth must be <empty> or '*' or an integer
		if [ ! -z "${depth}" ] && ! echo -n  "${depth}" |grep -E "^(\*|[0-9]+)$" >/dev/null 2>&1
		then
			echo "Error : the depth value '${depth}' is not valid" >> "${log_file}"
			exit 1
		fi

		# run the snapshooter versioner (in background)
		(
			echo "Watching dir '${f_path}' for file changes ..." >> "${log_file}"
			exec "${snapshooter_versioner_bin}" "${f_path}" "${delay}" "${depth}" 'true' >> "${log_file}" 2>&1
		) &
		children_pid="${children_pid} ${!}"

		#echo "Traping EXIT signal ..." >> "${log_file}"
		trap "
			trap '' INT TERM
			echo '[`date '+%Hh%Mm%Ss'`] Traped EXIT signal ...' >> '${log_file}'
			cleanExit '${children_pid}'
		" EXIT
		#echo "Traping INT and TERM signals ..." >> "${log_file}"
		trap "
			trap '' EXIT
			echo '[`date '+%Hh%Mm%Ss'`] Traped INT or TERM signal ...' >> '${log_file}'
			cleanExit '${children_pid}'
		" INT TERM

		# increase the number of folder monitored
		number_of_monitored_folders=`expr ${number_of_monitored_folders} '+' 1`

		# sleep a little to let the child checks if an other child is watching the same folder (or contained folder)
		sleep 2
	fi
	IFS="
"
done
IFS=" "
if [ "${number_of_monitored_folders}" -gt 0 ]
then
	echo "${number_of_monitored_folders} folders monitored for files changes" >> "${log_file}"
	# wait for all children to finish
	echo "Waiting for versioners to end (PIDs are :${children_pid}) ..." >> "${log_file}"
	#wait ${children_pid} >> "${log_file}" 2>&1
	wait >> "${log_file}" 2>&1
# no folder file
else
	echo "No folder to monitor" >> "${log_file}"
fi
