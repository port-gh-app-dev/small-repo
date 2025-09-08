#!/bin/bash

# Store the original content of port.yml
original_content=$(<port.yml)

# Overwrite port.yml with the first instance of the content
echo "$original_content" > port.yml

# Append the content 999 more times, separated by '---'
for i in {1..999}
do
  echo "---" >> port.yml
  echo "$original_content" >> port.yml
done
