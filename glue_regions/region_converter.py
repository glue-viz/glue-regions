import numpy as np
import os
import regions

from glue.config import data_factory
from glue.core.data_factories import has_extension
from glue.core.roi import CircularROI, PointROI, RectangularROI, PolygonalROI
from glue.core.data import Data
from glue.core.component import Component

from glue.config import layer_action
from glue.core.subset import RoiSubsetState, MultiOrState

def reg_to_roi(reg):
    """
    Function to convert a region to an ROI
    This might be implementable as a dictionary/registry,
    but hard-coding it isn't more difficult...
    """

    if isinstance(reg, regions.CirclePixelRegion):
        return CircularROI(xc=reg.center.x, yc=reg.center.y, radius=reg.radius)
    elif isinstance(reg, regions.PointPixelRegion):
        return PointROI(x=reg.center.x, y=reg.center.y)
    elif isinstance(reg, regions.RectanglePixelRegion):
        if reg.angle == 0:
            xmin, xmax = reg.center.x - reg.width / 2, reg.center.x + reg.width / 2
            ymin, ymax = reg.center.y - reg.height / 2, reg.center.y + reg.height / 2
            return RectangularROI(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
        else:
            if hasattr(reg, 'corners'):
                xverts = [c[0] for c in reg.corners]
                yverts = [c[1] for c in reg.corners]
                return PolygonalROI(vx=xverts, vy=yverts)
            else:
                raise NotImplementedError("Rectangles need to convert to polygons.")
    elif isinstance(reg, regions.PolygonPixelRegion):
        return PolygonalROI(vx=reg.vertices.x, vy=reg.vertices.y)
    else:
        raise NotImplementedError("Region {0} not recognized".format(reg))

def roi_to_reg(roi):
    """
    Function to convert a ROI to a region
    """

    if isinstance(roi, CircularROI):
        return regions.CirclePixelRegion(center=(roi.xc, roi.yc, radius=roi.radius))
    elif isinstance(roi, PointROI):
        return regions.PointRegion(center=(roi.x, roi.y))
    elif isinstance(roi, PolygonalROI):
        return regions.PolygonPixelRegion(vertices=list(zip(roi.vx, roi.vy)))
    else:
        raise NotImplementedError("ROI {0} not recognized".format(roi))


class RegionData(Data):

    def to_subset(self, wcs):
        print("thing with to_subset: ",self)
        preg = [reg.to_pixel(wcs)
                if hasattr(reg, 'to_pixel')
                else reg
                for reg in self['regions']]

        subsets = [reg_to_roi(reg) for reg in preg]
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
