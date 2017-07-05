
# 这个仓库研究如何使用开源技术来实现TMS(Tile Map Service)



## vector： /vector

- globalmaptiles.py 球面墨卡托投影和普通圆柱投影下瓦片编码和地理坐标转换类（详细见注释）

- vector_tile.py： 简易的*TMS*服务器，服务器支持提供*球面墨卡托投影*的瓦片和*普通圆柱投影*的瓦片（通过设置*profile*参数指定）(瓦片编码是谷歌风格的编码，原点位于左上角)。

主流存在两种类型的地图瓦片：
1. *球面墨卡托投影*下的256px*256px的地图瓦片
2. *普通圆柱投影*下的512px*256px的地图瓦片

两种投影分别使用256px*256px和512px*512px瓦片的原因是：在球面墨卡托投影下，全球范围被展绘成一个正方形（纬度大于85的部分被截去），而在普通圆柱投影中，全球范围被绘制成一个长宽比为2:1的长方形上。为了保证将地图完整不变性地绘制在瓦片上，必须要求瓦片形状和地图范围的形状相似。所以，在球面墨卡托投影下，瓦片的形状一定是正方形，而在普通圆柱投影下的瓦片形状是长宽比为2：1的长方形。一般的设定是256px*256px和512px*256px。



- ne_110m_admin_0_countries: 示例矢量数据
- html： 演示球面墨卡托瓦片的前端页面
- result： 缓存动态生成的瓦片

### 技术栈

- mapnik: 地图渲染库

### 思路

1. 使用mapnik配置地图样式，数据源投影，瓦片投影
2. 对于一个瓦片请求/z/x/y，首先解析出瓦片的比例尺级别z,瓦片的列号x,瓦片的行号y。然后根据投影的类型，可以确定出/z/x/y所对应的地理范围。将地图缩放到指定的地理范围然后绘制到.png图像上并返回



### 球面墨卡托投影的瓦片（256px*256px）

- /0/0/0 全球

![0/0/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator0_0_0.png)
- /1/0/0 西北半球

![1/0/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator1_0_0.png)
- /1/0/1 西南半球

![1/0/1](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator1_0_1.png)
- /1/1/0 东南半球

![1/1/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator1_1_0.png)
- /1/1/1 东北半球

![1/1/1](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator1_1_1.png)


### 地理投影的瓦片 (512px*256px)
- /0/0/0 全球 

![0/0/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic0_0_0.png)
- /1/0/0 西北半球

![1/0/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic1_0_0.png)
- /1/0/1 西南半球

![1/0/1](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic1_0_1.png)
- /1/1/0 东南半球

![1/1/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic1_1_0.png)
- /1/1/1 东北半球

![1/1/1](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic1_1_1.png)

## raster

- gdal2tiles.py: gdal类库下提供的一个使用栅格地图生成地图瓦片的脚本
- gdal2tiles_parallel.py: gdal2tiles.py的多进程版本


### 思路：

1. 根据瓦片的投影类型对输入栅格地图进行重投影
2. 根据指定的最大比例尺级别，计算出该级别下的所有瓦片编码，再利用瓦片编码反算地理范围，然后使用地理范围和栅格图像的geotransform计算出栅格范围，提取出指定的范围，然后根据投影类型，重采样到256 * 256或512 * 256
3. 对于步骤2生成的瓦片，将相邻的4个瓦片镶嵌，然后重采样到256*256，得到低级比例尺的瓦片
4. 细节请见注释

### 工作流：

1. 使用gdaldem工具配置栅格图像的样式（gdal2tiles工具只支持RGB或者RGBA类型的输入）配置方法见[gdaldem彩色合成研究](http://note.youdao.com/share/?id=092866af9684899725110b81a6e57d08&type=note#/)。
2. 使用gdal2tiles生成瓦片，细节见[gdal2tiles瓦片生产研究](http://note.youdao.com/share/?id=0e8aee9c27a99b01ff49e039cb936aeb&type=note#/)

## 补充

关于地图投影的细节请见doc/