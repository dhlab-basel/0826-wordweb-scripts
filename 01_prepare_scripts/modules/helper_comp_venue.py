# Regex library
import re
# system library
import sys


def info(text, line, csv_file):

    data = {}
    data_type = ""

    venue_info = re.search("^(#008\d{3})\s(.*)", text)
    company_info = re.search("^(#009\d{3})\s(.*)", text)

    if venue_info:
        data = {
            "venueInternalId": venue_info.group(1),
            "venueTitle": venue_info.group(2)
        }
        data_type = "venue"
    elif company_info:
        data = {
            "companyInternalId": company_info.group(1),
            "companyTitle": company_info.group(2)
        }
        data_type = "company"
    else:
        print("FAIL helper comp_venue", text, csv_file, line)
        raise SystemExit(0)

    return data, data_type
