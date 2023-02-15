#!/bin/bash

# Define variables
path="/path/to/search"
mail="example@example.com"
today=$(date +%Y-%m-%d)
next_day=$(date -d "$today +1 day" +%Y-%m-%d)
files=""

# Search for txt files in the specified path and its subdirectories
for file in $(find $path -name "*.txt"); do
  # Check if the file contains review information
  if grep -q "Review: " "$file"; then
    # If review information is present, check if it's for today
    if grep -q "Review: $today" "$file"; then
      # Add the file to the list of files
      files="$files\n$file"
    fi
  else
    # If review information is not present, add it for the next day
    echo -e "\nReview: $next_day" >> "$file"
  fi
done

# If at least one file was found
if [ ! -z "$files" ]; then
  # Send an email to the specified address with a list of all matching files
  echo -e "The following files contain a review with the date $today:\n$files" | sendmail -t $mail
else
  echo "No files with a review for today were found."
fi
