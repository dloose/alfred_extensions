#!/bin/bash

for plist in $(find . -maxdepth 2 -mindepth 2 -name 'info.plist' -type f); do
    dir=$(dirname "${plist}")
    name=$(plutil -convert json "${plist}" -o - | jq -r .name | tr -d '/ ')
    echo -n "Creating ${name} from ${dir}"
    ( \
        zip -r "${name}.alfredworkflow" alfred >/dev/null 2>&1; \
        cd "${dir}"; \
        zip -r "../${name}.alfredworkflow" . >/dev/null 2>&1 \
    )
    echo ...done
done
