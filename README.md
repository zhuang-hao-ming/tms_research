## 
这个仓库研究如何使用开源技术来实现TMS(Tile Map Service)

## vector： /vector

- globalmaptiles.py 球面墨卡托投影和普通圆柱投影下瓦片编码和地理坐标转换类

- vector_tile.py： 简易的*TMS*服务器，服务器支持提供*球面墨卡托投影*的瓦片和*普通圆柱投影*的瓦片（通过设置*profile*参数指定）(瓦片编码是谷歌风格的编码，原点位于左上角)。

主流存在两种类型的地图瓦片：
1. *球面墨卡托投影*下的256px*256px的地图瓦片
2. *普通圆柱投影*下的512px*256px的地图瓦片

两种投影分别使用256px*256px和512px*512px瓦片的原因是：在球面墨卡托投影下，全球范围被展绘成一个正方形（纬度大于85的部分被截去），而在普通圆柱投影中，全球范围被绘制成一个长宽比为2:1的长方形上。为了保证将地图完整不变性地绘制在瓦片上，必须要求瓦片形状和地图范围的形状相似。所以，在球面墨卡托投影下，瓦片的形状一定是正方形，而在普通圆柱投影下的瓦片形状是长宽比为2：1的长方形。一般的设定是256px*256px和512px*256px

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
