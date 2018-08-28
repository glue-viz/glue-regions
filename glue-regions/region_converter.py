import regions

from glue.config import data_factory
from glue.core.data_factories import has_extension
from glue.core.roi import CircularROI
from glue.core.data import Data



@data_factory('DS9 Region File', has_extension('reg'), default='reg')
def ds9_region(filename):
    reg = regions.read_ds9(filename)




