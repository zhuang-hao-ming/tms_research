import mapnik
import time

if __name__ == '__main__':
    start = time.time()
    m = mapnik.Map(256, 256)
    m.srs = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    s = mapnik.Style()
    r = mapnik.Rule()
    raster_symbolizer = mapnik.RasterSymbolizer()
    
    raster_symbolizer.colorizer = mapnik.RasterColorizer(mapnik.COLORIZER_LINEAR, mapnik.Color("transparent"))
    
    raster_symbolizer.colorizer.add_stop(0.0, mapnik.Color("black"))
    raster_symbolizer.colorizer.add_stop(1.0, mapnik.Color("white"))
    
    print -9999, raster_symbolizer.colorizer.get_color(-9999)
    print 0.0, raster_symbolizer.colorizer.get_color(0.0)
    print 1.0, raster_symbolizer.colorizer.get_color(1.0)
    print 0, raster_symbolizer.colorizer.get_color(0)
    print 1, raster_symbolizer.colorizer.get_color(1)
    print 0.5, raster_symbolizer.colorizer.get_color(0.5)

    r.symbols.append(raster_symbolizer)

    s.rules.append(r)

    m.append_style('raster_style', s)

    lyr = mapnik.Layer('urban')
    lyr.datasource = mapnik.Gdal(base='./', file='urban19901.tif', band=1)
    lyr.styles.append('raster_style')
    m.layers.append(lyr)
    m.zoom_all()
    mapnik.render_to_file(m, 'test1.png', 'png')

    print(time.time() - start)