#!/bin/bash
function make_backup {
    target="$1"
    backup="$1.backup"
    test -f $target && echo "backup $target to $backup" && mv $target $backup
    return 0
}

function restore_backup {
    target="$1"
    backup="$1.backup"
    test -f $backup && echo "restoring $backup to $target" && mv $backup $target
    return 0
}

for kind in "Entry" "Logo"; do
    output="${kind}.xml"
    make_backup ${output} && appcfg.py download_data \
        --config_file=bulkloader.yaml \
        --filename=${output} \
        --log_file=bulkloader.log \
        --result_db_filename=bulkloader-results.${kind}.sqlite3 \
        --db_filename=bulkloader-progress.${kind}.sqlite3 \
        --kind=${kind} \
        . || { restore_backup ${output} && exit 1; }
done

