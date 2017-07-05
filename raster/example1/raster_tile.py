import mapnik


if __name__ == '__main__':
    m = mapnik.Map(256, 256)
    m.srs = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    s = mapnik.Style()
    r = mapnik.Rule()
    raster_symbolizer = mapnik.RasterSymbolizer()
    
    raster_symbolizer.colorizer = mapnik.RasterColorizer(mapnik.COLORIZER_LINEAR, mapnik.Color("transparent"))
    raster_symbolizer.colorizer.add_stop(0.0, mapnik.Color('#000000'))
    raster_symbolizer.colorizer.add_stop(1.0, mapnik.Color('#ffffff'))
    # white = mapnik.Color('#ffffff')
    # stop_white = mapnik.ColorizerStop(1, mapnik.COLORIZER_LINEAR, white)
    # black = mapnik.Color('#000000')    
    # stop_black = mapnik.ColorizerStop(0, mapnik.COLORIZER_LINEAR, black)
    # raster_symbolizer.colorizer.add_stop(stop_black)
    # raster_symbolizer.colorizer.add_stop(stop_white)
    r.symbols.append(raster_symbolizer)

    s.rules.append(r)

    m.append_style('raster_style', s)

    lyr = mapnik.Layer('urban')
    lyr.datasource = mapnik.Gdal(base='./', file='urban19901.tif')
    lyr.styles.append('raster_style')
    m.layers.append(lyr)
    m.zoom_all()
    mapnik.render_to_file(m, 'test1.png', 'png')

