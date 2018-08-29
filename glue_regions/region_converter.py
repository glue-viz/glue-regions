import numpy as np
import os
import regions

from glue.config import data_factory
from glue.core.data_factories import has_extension
from glue.core.roi import CircularROI, PointROI
from glue.core.data import Data
from glue.core.component import Component

from glue.config import layer_action
from glue.core.subset import RoiSubsetState, MultiOrState

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

@layer_action(label='Convert regions to subset')
def layer_to_subset(selected_layers, data_collection):

    # loop over selected  layers
    for layer in selected_layers:
        if isinstance(layer, RegionData):
            for data in data_collection:
                if hasattr(data, 'coords') and hasattr(data.coords, 'wcs'):
                    list_of_rois = layer.to_subset(data.coords.wcs)

                    roisubstates = [RoiSubsetState(data.coordinate_components[1],
                                                   data.coordinate_components[0],
                                                   roi=roi
                                                  )
                                    for roi in list_of_rois]
                    composite_substate = roisubstates[0]
                    if len(list_of_rois) > 1:
                        composite_substate = MultiOrState(roisubstates)
                    else:
                        composite_substate = roisubstates[0]
                    subset_group = data_collection.new_subset_group(label=layer.label,
                                                                    subset_state=composite_substate)
