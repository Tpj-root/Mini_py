#!/bin/bash

URL="https://tnresults.nic.in/rdtpex.asp"
COOKIE='ASPSESSIONIDCCBABBQQ=KIAACIMAMCIHPCCGGIFIHCAN; ASPSESSIONIDSCCDCCSB=GPOGLFMAHNOBFALDIMDDCOFO; ASPSESSIONIDAASATBTT=NLEMFCMAKADOEEGNOKIJAOBK; ASPSESSIONIDSQTQQSDT=PICPFCMAAAIGGEPKHMPELFED'

for REGNO in $(seq 1465009 1465009); do
  for year in 2007 2008; do
    if [ "$year" == "2007" ]; then
      start_month=1
      end_month=12
    else
      start_month=1
      end_month=12
    fi

    for month in $(seq -w $start_month $end_month); do
      for day in $(seq -w 1 31); do
        DOB="${day}%2F${month}%2F${year}"
        DOB_CLEAN="${day}_${month}_${year}"
        TMPFILE="tmp_output.html"

        echo "Checking REGNO: $REGNO DOB: ${DOB_CLEAN}"

        curl "$URL" -X POST \
          -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0' \
          -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
          -H 'Accept-Language: en-US,en;q=0.5' \
          -H 'Accept-Encoding: gzip, deflate, br, zstd' \
          -H 'Content-Type: application/x-www-form-urlencoded' \
          -H 'Origin: https://tnresults.nic.in' \
          -H 'Connection: keep-alive' \
          -H 'Referer: https://tnresults.nic.in/rdtpex.htm' \
          -H "Cookie: $COOKIE" \
          -H 'Upgrade-Insecure-Requests: 1' \
          -H 'Sec-Fetch-Dest: document' \
          -H 'Sec-Fetch-Mode: navigate' \
          -H 'Sec-Fetch-Site: same-origin' \
          -H 'Sec-Fetch-User: ?1' \
          -H 'Priority: u=0, i' \
          --data-raw "regno=$REGNO&dob=$DOB&B1=Get+Marks" \
          -o "$TMPFILE"

        if grep -q "$REGNO" "$TMPFILE"; then
          mv "$TMPFILE" "${DOB_CLEAN}_${REGNO}.html"
          echo "✅ Found and saved: ${DOB_CLEAN}_${REGNO}.html"
          #exit 0
          break 3
        #else
        #  rm -f "$TMPFILE"
        #  echo "❌ Not found for REGNO: $REGNO DOB: ${DOB_CLEAN}"
        #fi
        else
          rm -f "$TMPFILE"
          echo "❌ Not found for REGNO: $REGNO DOB: ${DOB_CLEAN}"
          if [ "$DOB_CLEAN" = "31_6_2008" ]; then
            echo "REGNO: $REGNO DOB: ${DOB_CLEAN} not in the list" >> not_found_list.txt
          fi
        fi




        sleep 1
      done
    done
  done
done
