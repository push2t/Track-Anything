from photoshop import Session
from PIL import Image
import glob

def subdir_stack_to_psd(stackdir, outfile):
    print("opening images in stackdir %s" % (stackdir))
    files = glob.glob(stackdir + "/*")
    print("discovered %d files: %s" % (len(files), files))

    ## peek at first file to sniff resolution
    _f = Image.open(files[0])
    width, height = (_f.width, _f.height)
    _f.close()

    with Session() as ps:

        ps.app.preferences.rulerUnits = ps.Units.Pixels
        ps.app.documents.add(width, height, name="masked")

        for f in files:

            # double check dimensions of this file match our first sniffed
            _f = Image.open(files[0])
            _width, _height = (_f.width, _f.height)
            _f.close()
            if _width != width or height != height:
                raise ValueError("file %s (%d x %d) did not match expected sniffed resolutions %d x %d" % (f, _width, _height, width, height))

            print("inserting file %s (%d x %d)  as layer" % (f, _width, _height))
            desc = ps.ActionDescriptor
            desc.putPath(ps.app.charIDToTypeID("null"), f)
            event_id = ps.app.charIDToTypeID("Plc ")  # `Plc` need one space in here.
            ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
            print("successfully inserted %s as layer" % (f))

        # fuck the background layer off
        bg = ps.active_document.artLayers.getByName("Background")
        bg.remove()


        # name the layers in order of insertion
        i = 1
        for al in reversed(list(ps.active_document.artLayers())):
            al.name = "%d" % (i)
            i += 1

        
        # convert from smart object into dumb layers
        descriptor = ps.ActionDescriptor
        idplacedLayerConvertToLayers = ps.app.stringIDToTypeID("placedLayerConvertToLayers")
        ps.app.executeAction(idplacedLayerConvertToLayers, descriptor)
        ps.active_document.rasterizeAllLayers()

        # save it
        options = ps.PhotoshopSaveOptions()
        doc = ps.active_document
        layers = doc.artLayers
        doc.saveAs(outfile, options, True)
        doc.close()
