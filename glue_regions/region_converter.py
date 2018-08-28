import numpy as np
import regions

from glue.config import data_factory
from glue.core.data_factories import has_extension
from glue.core.roi import CircularROI
from glue.core.data import Data
from glue.core.component import Component



@data_factory('DS9 Region File', has_extension('reg'), default='reg')
def ds9_region(filename):
    reg = regions.read_ds9(filename)


    comp = Component(np.ones(len(reg), dtype='bool'))
    data = Data(label='Regions from {0}'.format(filename),
                regions=component)

    return data
