from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os

import mapnik
from sphericalmercator import SphericalMercator

from osgeo import osr

p1 = osr.SpatialReference()
p1.ImportFromEPSG(4326)
p2 = osr.SpatialReference()
p2.ImportFromEPSG(3857)
transform = osr.CoordinateTransformation(p1, p2)


def get_map():
    m = mapnik.Map(256, 256)
    m.srs = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs'
    m.background = mapnik.Color('steelblue')
    s = mapnik.Style()
    r = mapnik.Rule()

    polygon_symbolizer = mapnik.PolygonSymbolizer()
    polygon_symbolizer.fill = mapnik.Color('#f2eff9')
    r.symbols.append(polygon_symbolizer)

    line_symbolizer = mapnik.LineSymbolizer()
    mapnik.LineSymbolizer(mapnik.Color('green'),0.1)
    r.symbols.append(line_symbolizer)
    s.rules.append(r)
    m.append_style('My Style', s)
    
    ds = mapnik.Shapefile(file='./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')

    layer = mapnik.Layer('world')
    # layer.srs = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs'
    layer.datasource = ds
    layer.styles.append('My Style')
    m.layers.append(layer)
    return m 

PORT_NUM = 8080
m = get_map()
merc = SphericalMercator(levels=18, size=256)


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        arr = self.path.split('/')
        z=0
        x=0
        y=0
        if len(arr) == 4:
            z = int(arr[1])
            x = int(arr[2])
            y = int(arr[3])

        try: 

            envelope1 = merc.xyz_to_envelope(x=x, y=y, zoom=z)                    
            minx, miny, z = transform.TransformPoint(envelope1[0], envelope1[1])
            maxx, maxy, z = transform.TransformPoint(envelope1[2], envelope1[3])
            extent =  mapnik.Box2d(minx, miny, maxx, maxy)
            
            
            
            m.zoom_to_box(extent)
            #m.maximum_extent = extent
            file_name = './result/world{0}_{1}_{2}.png'.format(z, x, y)
            mapnik.render_to_file(m, file_name, 'png')

            
            f = open(file_name, 'rb')
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(404, 'File Not Found')            
        return



def main():
    try:
        server = HTTPServer(('', PORT_NUM), MyHandler)
        print('Started httpserver on port', PORT_NUM)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()