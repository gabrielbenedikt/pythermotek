# pythermotek
python class to interface with thermotek chillers

# install
'''
git clone git@github.com:gabrielbenedikt/pythermotek.git  
cd pythermotek  
pip3 install .  
'''

# usage

'''python
from thermotek import T255P, T257P
dev = T257P('/dev/ttyUSB0')
dev.get_supply_t()
'''
