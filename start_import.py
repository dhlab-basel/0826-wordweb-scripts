# system library
import sys

# defining path for module imports
sys.path.append("01_prepare_scripts/")
sys.path.append("01_prepare_scripts/modules/")
sys.path.append("02_import_scripts/")

# module import for preparing data
import prepare as prep
# module import for importing the data from jsons to knora
import import_to_knora as imp


# preparing the data and storing them as jsons in folder 00_data_as_json
prep.start()
# importing the data from json to knora
imp.start()
