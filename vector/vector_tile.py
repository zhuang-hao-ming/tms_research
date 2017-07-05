# -*- encoding: utf-8
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os

import mapnik

from globalmaptiles import GlobalMercator, GlobalGeodetic
from osgeo import osr


#profile = 'mercator'
profile = 'geodetic'

if profile == 'mercator':
    map_width = 256
    map_height = 256
    map_srs = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs' 
    merc = GlobalMercator()
elif profile == 'geodetic':
    map_width = 512
    map_height = 256
    map_srs = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    merc = GlobalGeodetic()

def get_map():
    m = mapnik.Map(map_width, map_height)

    
    m.srs = map_srs # the output projection

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
    # layer.srs = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs' # the input projection, it mush be the same as the source's projection
    # '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    layer.datasource = ds
    layer.styles.append('My Style')
    m.layers.append(layer)
    return m 

PORT_NUM = 8080
m = get_map()





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
            
            # z/x/y 反算 bound：
            # 计算地图分辨率：
            # res = initRes / 2 ** z
            # 计算瓦片角点到地图左上角的距离
            # x * 256 * res = dist_min_x,
            # y * 256 * res = dist_min_y ,
            # (x + 1) * 256 * res = dist_max_x,
            # (y + 1) * 256 * res = dist_max_y
            # 计算瓦片角点投影坐标
            # tile_x_min = map_x_min + dist_min_x
            # tile_y_min = map_y_max - dist_min_y
            # tile_x_max = map_x_min + dist_max_x
            # tile_y_max = map_y_max - dist_max_y
            # 反算wgs84坐标 
            # 
            # 由于在球面墨卡托投影中，我们令纵横分辨率相同，所以正方形瓦片覆盖的地理范围是正方形的，可以无变形的绘制到正方形瓦片上。 
            # 
            
            if profile == 'mercator':
                new_x, new_y = merc.GoogleTile(x, y, z)
                minx, miny, maxx, maxy = merc.TileBounds(new_x, new_y, z)
                extent =  mapnik.Box2d(minx, miny, maxx, maxy)
            elif profile == 'geodetic':                
                minx, miny, maxx, maxy = merc.TileBounds(x, y, z)
                
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