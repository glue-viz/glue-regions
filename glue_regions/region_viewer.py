from glue.viewers.matplotlib.layer_artist import MatplotlibLayerArtist
from glue.viewers.matplotlib.state import MatplotlibLayerState

class RegionLayerArtist(MatplotlibLayerArtist):

    _layer_state_cls = MatplotlibLayerState

    def __init__(self, axes, viewer_state, layer_state=None, layer=None):

        super(RegionLayerArtist, self).__init__(axes,
                                                viewer_state,
                                                layer_state=layer_state,
                                                layer=layer)

        # if the region file is in WCS, the data must have a valid WCS,
        # but if it's in pixel coordinates, we don't need a WCS.
        # We don't have a clean fail case defined here yet.
        if hasattr(viewer_state.reference_data.coords, 'wcs'):
            wcs = viewer_state.reference_data.coords.wcs
        else:
            wcs = None

        # Convert each of the regions to a patch in the appropriate image
        # coordinates.
        artists = [reg.to_pixel(wcs).as_patch()
                   if hasattr(reg, 'to_pixel')
                   else reg.as_patch()
                   for reg in layer['regions']]

        self.mpl_artists = artists

        for artist in self.mpl_artists:
            axes.add_patch(artist)

        print("Initialized a RegionLayerArtist")

    def get_layer_color(self):
        return 'b'
        #colors = [artist.color for artist in self.mpl_artists]
        #if len(set(colors)) == 1:
        #    return colors[0]
        #else:
        #    return None

    def update(self, view=None):
        self.redraw()

