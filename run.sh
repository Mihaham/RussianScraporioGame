#!/bin/bash
#sudo ./run.sh --input_folder  --extension py --backup_folder backup --backup_archive_name backup.tar.gz
path=$(pwd)
while [ -n "$1" ]
do
case "$1" in
--extension) extension="$2"
shift ;;
--backup_folder) backup_folder="$2"
shift ;;
--backup_archive_name) backup_archive_name="$2"
shift ;;
--input_folder) input_folder="$2"
shift ;;
esac
shift
done

mkdir "$backup_folder" > /dev/null

recoursive_function() {
for file in $1
do
if [ -d "$file" ]
then
	last_dir=$(basename "$file")
	if [[ ($last_dir != "$backup_folder") && ($last_dir != "venv")]]
	then
		mkdir "$2"/"$last_dir" > /dev/null
		cd "$last_dir" || return
		recoursive_function "$file/*" "$2/$last_dir"
		cd ..
	fi
elif [ -f "$file" ]
then
	filename=$(basename "$file")
	if [[ $filename == *.$extension ]]
	then
		cat "$filename" >> "/mnt/e/RussianScraporioGame/backup.py"
	fi
fi
done
}

cd "$input_folder" || return
recoursive_function "$input_folder/*" "$path/$backup_folder"
cd "$path"/"$backup_folder" || return
cd ..

echo "done"