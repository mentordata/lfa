#!/bin/bash

table_name="my_table"
column_name="date_column"

# checking whether two arguments have been provided
if [ "$#" -ne 2 ]; then
        echo "Usage: $0 date1 date2"
        exit 1
fi

# creating proper date format
start_date=$(date -d "$1" +"%s")
end_date=$(date -d "$2" +"%s")

# creating INSERT query

for ((i=$start_date;i<=$end_date;i+=86400)); do
        current_date=$(date -d "@$i" +"%Y-%m-%d")

        query="INSERT INTO $table_name ($column_name) VALUES ('$current_date');"

        echo $query
done
