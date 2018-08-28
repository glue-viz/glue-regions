def setup():
    from .region_viewer import RegionLayerArtist

    from glue.config import data_layer_registry
    from glue.viewers.image.viwer import MatplotlibImageMixin

    data_layer_registry.add((RegionLayerArtist, MatplotlibImageMixin))
