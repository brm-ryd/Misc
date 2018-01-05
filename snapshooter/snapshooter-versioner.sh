#!/bin/sh

set -o errexit
set -o nounset

#--- variables -----------------------------------------------------
NAME=snapshooter
CONF_DIR=/etc/${NAME}
CONF_FILE=${CONF_DIR}/${NAME}.conf



#--- configuration -------------------------------------------------
if [ -f "${CONF_FILE}" ]
then
	. "${CONF_FILE}"
fi



#--- get parameters from configuration -----------------------------
# folders
log_dir=${LOG_DIR:-/var/log/${NAME}}
datas_dir=${DATAS_DIR:-/var/${NAME}}
backup_dir=${BACKUP_DIR:-${datas_dir}/backups}
# files
pid_file=${PID_FILE:-/var/run/${NAME}.pid}
process_file=${PROCESS_FILE:-${datas_dir}/process.tmp}



#--- check / create folders and files ------------------------------
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



#--- functions -----------------------------------------------------
# get the real path of a file or directory
getRealPath() {
	readlink -f "${1:-}" |sed 's/\\$//'
}

# get a uid of the file or dir from its real path
getUid() {
	sha1sum <<EOF |awk '{print $1}'
`getRealPath "${1:-}"`
EOF
}

# get a duration text fomr a time in seconds
getDurationText() {
	total_sec=${1:-}
	if ! echo -n "${total_sec}" |grep -E '^[0-9]+$' >/dev/null 2>&1
	then
		return
	else
		if [ ${total_sec} -eq 0 ]
		then
			echo "0 sec"
			return
		fi
	fi
	sec=0
	min=0
	hour=0
	day=0
	if [ ${total_sec} -gt 59 ]
	then
		sec=`expr ${total_sec} '%' 60`
		total_sec=`expr ${total_sec} '-' ${sec}`
		total_min=`expr ${total_sec} '/' 60`
		if [ ${total_min} -gt 59 ]
		then
			min=`expr ${total_min} '%' 60`
			total_min=`expr ${total_min} '-' ${min}`
			total_hour=`expr ${total_min} '/' 60`
			if [ ${total_hour} -gt 23 ]
			then
				hour=`expr ${total_hour} '%' 24`
				total_hour=`expr ${total_hour} '-' ${hour}`
				day=`expr ${total_hour} '/' 24`
			else
				hour=${total_hour}
			fi
		else
			min=${total_min}
		fi
	else
		sec=${total_sec}
	fi
	duration_time_text=''
	if [ ${day} -gt 0 ]
	then
		if [ ${day} -eq 1 ]
		then
			duration_time_text="${day} day"
		else
			duration_time_text="${day} days"
		fi
	fi
	if [ ${hour} -gt 0 ]
	then
		duration_time_text="${duration_time_text} ${hour} hour"
	fi
	if [ ${min} -gt 0 ]
	then
		duration_time_text="${duration_time_text} ${min} min"
	fi
	if [ ${sec} -gt 0 ]
	then
		duration_time_text="${duration_time_text} ${sec} sec"
	fi
	duration_time_text=`echo -n "${duration_time_text}" |sed 's/^\s*//'`
	echo "${duration_time_text}"
}

# return the number of parent dirs
getNumberOfParentDir() {
	echo -n "${1:-}" |sed 's/\/$//' |tr -dc '/' |wc -c
}

# return the number of dir between a folder and its parent folder specified
getGapDirNumber() {
	expr `getNumberOfParentDir "${1:-}"` '-' `getNumberOfParentDir "${2:-}"`
}

# return 0 if a folder is contained in the other
# return 1 else
isContained() {
	fld=${1:-}
	ctn=${2:-}
	dpt=${3:-}
	# if they are not null
	if [ ! -z "${fld}" -a ! -z "${ctn}" ]
	then
		# remove the trailing slash '/'
		fld=`echo -n "${fld}" |sed 's/\/$//'`
		container=`echo -n "${ctn}" |sed 's/\/$//'`
		# if the path of the folder begins with the path of the container
		if echo -n "${fld}" |grep "^${ctn}" >/dev/null 2>&1
		then
			# if the depth is specified and not *
			if [ ! -z "${dpt}" -a "${dpt}" != "*" ]
			then
				# the folder is in the depth of the container
				if [ "`getGapDirNumber "${fld}" "${ctn}"`" -lt "${dpt}" ]
				then
					return 0
				fi
			else
				return 0
			fi
		fi
	fi
	return 1
}

# echo 1 if the folder is currently watched
# echo 2 if the folder is in a watched folder
# echo 3 if the folder contains a folder that is currently watched
# echo 0 else (not already watched)
isFolderAlreadyWatched() {
	folder=${1:-}
	depth=${2:-}
	# if the folder is in the process file
	if awk '{print $2}' "${process_file}" |grep "^${folder}$" >/dev/null 2>&1
	then
		echo 1 && return
	fi
	# for each snapshooter-versioner process runing (and associated folder path)
	while read pid compared_path compared_depth
	do
		# if the folder is contained in the path
		if isContained "${folder}" "${compared_path}" "${compared_depth}"
		then
			echo 2 && return
		fi
		# if the folder contains the path
		if isContained "${compared_path}" "${folder}" "${depth}"
		then
			echo 3 && return
		fi
	done < "${process_file}"
	echo 0
}



#--- get parameters ------------------------------------------------
# folder to check for changes
f_path=${1:-}
# get the delay to check file changes, by default we set it to 5 minutes
f_delay=${2:-300}
# depth ? by default it monitors all sub-folders
depth=${3:-*}
# quiet ?
quiet=${4:-false}



#--- check parameters ----------------------------------------------
# if no parameters or too much were specified
if [ $# -eq 0 -o $# -gt 4 ]
then
	echo "USAGE : snapshooter-versioner <folder> <delay> <depth> <quiet>" >&2
	echo "WHERE : <folder> is the folder to check for file changes" >&2
	echo "        <delay> is the number of seconds between checks" >&2
	echo "        <depth> is the number of level of sub-folders to monitor (see man find '-maxdepth', '*' is all sub-folders)" >&2
	echo "        <quiet> set to 'true' means no output to STDOUT" >&2
	exit 1
fi
# if the folder doesn't exist
if [ ! -d "${f_path}" ]
then
	echo "Error : the folder '${f_path}' doesn't exist" >&2
	exit 1
# folder exists
else
	# we get its realpath (and removing the '/' at the end if there was one)
	f_path=`getRealPath "${f_path}"`
	# and hash it to use as a uid
	uid=`getUid "${f_path}"`
fi
# if the delay is not a number
if ! echo -n "${f_delay}" |grep -E '^[0-9]+$' >/dev/null 2>&1
then
	echo "Error : the delay specified '${f_delay}' is not a number" >&2
	exit 1
# delay is valid
else
	delay=${f_delay}
fi
# if the depth is specified but not valid
if [ ! -z "${depth}" ] && ! echo -n  "${depth}" |grep -E "^(\*|[0-9]+)$" >/dev/null 2>&1
then
	echo "Error : the depth specified '${depth}' is not valid" >&2
	exit 1
fi

[ ${quiet} != "true" ] && echo "#-- Saving file changes of directory '${f_path}' (with depth '${depth}') each '${f_delay}' sec ..."



#--- prevent from watching the same folder twice (or more) ---------
# if the folder is already watched
watched=`isFolderAlreadyWatched "${f_path}" "${depth}"`
if [ "${watched}" -eq 1 ]
then
	echo "Error : The folder '${f_path}' is already watched" >&2
	exit 1
elif [ "${watched}" -eq 2 ]
then
	echo "Error : The folder '${f_path}' is in a folder already watched" >&2
	exit 1
elif [ "${watched}" -eq 3 ]
then
	echo "Error : The folder '${f_path}' contains a folder already watched" >&2
	exit 1
fi



#--- backup path ---------------------------------------------------
# get the relative folder path by removing the first '/' of its real path
f_rel_path=`echo -n "${f_path}" |sed 's/^\///'`
# get the full backup path : add the relative folder to the base backup path
back_path=${backup_dir}/${f_rel_path}
[ ${quiet} != "true" ] && echo "backup to : ${back_path}"
# if the backup dir doesn't exist
if [ ! -d "${back_path}" ]
then
	# we create it
	mkdir -p "${back_path}"
fi



#--- update process list -------------------------------------------
# write the process pid and folder infos in the process file
echo "$$	${f_path}	${depth}" >> "${process_file}"



#--- timestamp file ------------------------------------------------
# we will check for file changes from this timestamp file
timestamp_file=${back_path}.timestamp
# if the timestamp file doesn't exist
if [ ! -f "${timestamp_file}" ]
then
	# we create it
	date '+%s' > "${timestamp_file}"
fi



#--- run in a loop -------------------------------------------------
while true
do
	#... start timer ......................................
	# in order to get a proper delay between loop
	# we need to substitute the time taken to run the loop to the delay
	# so we need to get the time the loop take
	# so we need start a timer
	timer_start=`date '+%s'`

	#... log file .........................................
	old_log_file=${log_file:-}
	log_file=${log_dir}/`echo -n "${f_rel_path}" |sed 's/\//_/g'`.log.`date '+%Y-%m-%d'`
	# if we need to change the log file (new or day has changed)
	if [ "${old_log_file}" != "${log_file}" ]
	then
		[ ${quiet} != "true" ] && echo "Log to : ${log_file}"
	fi
	# if the log file doesn't exist
	if [ ! -f "${log_file}" ]
	then
		# we create it
		echo "${NAME}-versioner log file" > "${log_file}"
		echo "#=========================================================" >> "${log_file}"
		echo "real folder path is  : ${f_path}" >> "${log_file}"
		echo "depth is             : ${depth}" >> "${log_file}"
		echo "uid is               : ${uid}" >> "${log_file}"
		echo "backup path is       : ${back_path}" >> "${log_file}"
	fi
	echo >> "${log_file}"
	echo "#------------------------------ `date '+%Hh%Mm%Ss'` ------------------------------" >> "${log_file}"
	echo >> "${log_file}"

	#... create the new timestamp file ................
	timestamp_file_new=${timestamp_file}.new
	date '+%s' > "${timestamp_file_new}"

	#... save changed files ...........................
	last_backup=`stat --format="%Y" "${timestamp_file}"`
	current_time=`date '+%s'`
	if [ ${current_time} -ne ${last_backup} ]
	then
		since=`expr ${current_time} '-' ${last_backup}`
	else
		since=0
	fi
	echo "saving changed files since `getDurationText "${since}"`..." >> "${log_file}"
	# get all changed files since the time specified
	number_of_changed_files=0
	# if the depth is specified and is not '*'
	depth_param=
	if [ ! -z "${depth}" -a "${depth}" != "*" ]
	then
		depth_param="-maxdepth ${depth}"
	fi
	for f in `
		find "${f_path}" ${depth_param} \
		-type f -newer "${timestamp_file}" -not -name "*.tmp" -not -name "*~" -not -name "*.part" \
		-o -type f -cnewer "${timestamp_file}" -not -name "*.tmp" -not -name "*~" -not -name "*.part"
	`
	do
		# if the file exists
		if [ -f "${f}" ]
		then
			number_of_changed_files=`expr ${number_of_changed_files} '+' 1`
			echo "   `basename "${f}"` has changed" >> "${log_file}"
			# get the realpath of the file
			f_r_path=`getRealPath "${f}"`
			# get the parent dir
			f_p_dir=`dirname "${f_r_path}"`
			# get the mode and ownership of the parent dir
			f_p_mode=`stat --format="%a" "${f_p_dir}"`
			f_p_owner=`stat --format="%U:%G" "${f_p_dir}"`
			# get the relative parent dir by removing the '/' at the begining (if there is one)
			f_p_rel_dir=`echo -n "${f_p_dir}" |sed 's/^\///'`
			# build the full parent dir backup
			f_p_back_path=${backup_dir}/${f_p_rel_dir}
			#echo "parent backup dir is : ${f_p_back_path}"
			# if the dir doesn't exist
			if [ ! -d "${f_p_back_path}" ]
			then
				# we create it
				mkdir -p "${f_p_back_path}"
			fi
			# restore its mode and ownership (if we can)
			chmod "${f_p_mode}" "${f_p_back_path}" >/dev/null 2<&1 ||echo >/dev/null
			chown "${f_p_owner}" "${f_p_back_path}" >/dev/null 2<&1 ||echo >/dev/null
			# buld the backup file path with the current time appended to its name
			f_back_path="${f_p_back_path}/`basename "${f_r_path}"`.`date '+%s'`"
			# copy the file to its backup path (try to preserve mode, ownership and timestamp)
			cp -pf "${f_r_path}" "${f_back_path}"
			echo "    > file saved to : ${f_back_path}" >> "${log_file}"
		else
			echo "   `basename "${f}"` has changed but doesn't exist !" >> "${log_file}"
		fi
	done

	echo "${number_of_changed_files} files changed" >> "${log_file}"

	# update the timestamp file
	mv -f "${timestamp_file_new}" "${timestamp_file}"

	#... get the time the loop has run ....................
	# end the timer
	timer_end=`date '+%s'`
	# duration (in secs)
	if [ ${timer_end} -ne ${timer_start} ]
	then
		duration=`expr ${timer_end} '-' ${timer_start}`
	else
		duration=0
	fi
	echo "the backup has taken `getDurationText "${duration}"`" >> "${log_file}"
	# get the time we need to sleep to maintain the delay
	if [ ${delay} -ne ${duration} ]
	then
		sleep_time=`expr ${delay} '-' ${duration}`
	else
		sleep_time=0
	fi
	# if the duration is greater than the delay
	if [ ${sleep_time} -lt 0 ]
	then
		echo "Warning : this backup was longer (`getDurationText "${duration}"`) than the delay (`getDurationText "${delay}"`)" >> "${log_file}"
		echo "Warning : increasing the delay by 10% more than this backup duration" >> "${log_file}"
		delay=`expr ${duration} '+' ${duration} '*' 10 '/' 100`
		echo "Warning : new delay is `getDurationText "${delay}"`" >> "${log_file}"
		sleep_time=0
	# duration lower than the delay
	else
		# if the delay is not as the original delay
		if [ ${delay} -ne ${f_delay} ]
		then
			echo "Warning : trying to get back to the original delay" >> "${log_file}"
			echo "Warning : decrease the delay by 10%" >> "${log_file}"
			delay=`expr ${delay} '-' ${delay} '*' 10 '/' 100`
			if [ ${delay} -lt ${f_delay} ]
			then
				delay=${f_delay}
				echo "Warning : came back to the orignal delay of `getDurationText "${delay}"`" >> "${log_file}"
			fi
			echo "Warning : the new delay is `getDurationText "${delay}"`" >> "${log_file}"
		fi
	fi

	(
		echo "sleeping `getDurationText "${sleep_time}"`..." >> "${log_file}"
		exec sleep "${sleep_time}"
	) &
	sleep_pid=${!}

	cleanExit() {
		# here the sleep process should have been killed
		# but if we see it is still runing
		if ps --pid ${sleep_pid} -o pid,ppid |grep -E "^[[:space:]]*${sleep_pid}[[:space:]]+$$[[:space:]]*$" >/dev/null 2>&1
		then
			# we kill it
			echo "Sleeping process still alive -> killing it ..." >> "${log_file}"
			kill "$sleep_pid"
		fi
		# remove new timestamp
		if [ -f "${timestamp_file_new}" ]
		then
			echo "removing new timestamp ..." >> "${log_file}"
			rm -f "${timestamp_file_new}"
		fi
		# remove the line of this process in the process file (looping until it's done)
		echo "removing line with pid $$ in the process file ..." >> "${log_file}"
		sed "/^$$\t.*$/ { d }" -i "${process_file}"
		while grep "^$$[[:space:]].*$" "${process_file}" >/dev/null 2>&1
		do
			echo "retrying ..." >> "${log_file}"
			sleep 0.2
			sed "/^$$\t.*$/ { d }" -i "${process_file}"
		done
		# log the end of the process
		echo "terminated" >> "${log_file}"
		# exiting
		exit
	}

	#echo "Traping EXIT signal ..." >> "${log_file}"
	trap "
		trap '' INT TERM
		echo 'Traped EXIT signal ...' >> '${log_file}'
		cleanExit
	" EXIT
	#echo "Traping INT and TERM signals ..." >> "${log_file}"
	trap "
		trap '' EXIT
		echo 'Traped INT or TERM signal ...' >> '${log_file}'
		cleanExit
	" INT TERM

	echo "Waiting until sleeping process is over ..." >> "${log_file}"
	wait >> "${log_file}" 2>&1
	echo "Stop waiting and continuing ..." >> "${log_file}"
	echo >> "${log_file}"
done
