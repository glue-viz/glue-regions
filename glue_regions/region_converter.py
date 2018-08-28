import numpy as np
import os
import regions

from glue.config import data_factory
from glue.core.data_factories import has_extension
from glue.core.roi import CircularROI, PointROI
from glue.core.data import Data
from glue.core.component import Component


class RegionData(Data):

    def to_subset(self, wcs):
        print("thing with to_subset: ",self)
        preg = [reg.to_pixel(wcs)
                if hasattr(reg, 'to_pixel')
                else reg
                for reg in self['regions']]

        subsets = [CircularROI(xc=reg.center.x,
                               yc=reg.center.y,
                               radius=reg.radius)
                   if isinstance(reg, regions.CirclePixelRegion)
                   else PointROI(x=reg.center.x,
                                 y=reg.center.y)
                   for reg in preg]
        return subsets



@data_factory('DS9 Region File', has_extension('reg'), default='reg')
def ds9_region(filename):
    reg = regions.read_ds9(filename)

    comp = Component(np.ones(len(reg), dtype='bool'))
    data = RegionData(label='Regions: {0}'.format(os.path.split(filename)[-1]),
                      regions=reg)

    return data
