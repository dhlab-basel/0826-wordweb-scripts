# Regex library
import re
# system library
import sys


def info(text, line, csv_file):

    data = {}
    data_type = ""

    venue_info = re.search("^(#008\d{3})\s(.*)_(.*)", text)
    company_info = re.search("^(#009\d{3})\s(.*)", text)

    if venue_info:
        data = {
            "venueInternalId": venue_info.group(1),
            "hasVenuePlace": venue_info.group(3)
        }
        data_type = "venue"
    elif company_info:
        data = {
            "companyInternalId": company_info.group(1),
            "companyTitle": company_info.group(2)
        }
        data_type = "company"
    else:
        data_type = "none"

    return data, data_type
