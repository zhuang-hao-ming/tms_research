## 
这个仓库研究如何使用开源技术来实现TMS(Tile Map Service)

## vector

vector目录下是利用矢量数据提供TMS服务的实现。
运行vector_tile.py文件即可以启动一个简易的TMS服务器，服务器支持提供球面墨卡托投影的瓦片和geodetic投影的瓦片（通过设置profile参数指定）。
示例数据存放在ne_110m_admin_0_countries文件夹下。
html文件夹下存放了使用球面墨卡托瓦片的一个前端页面
result缓存动态生成的瓦片

### 球面墨卡托投影的瓦片


- /0/0/0 
![0/0/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator0_0_0.png)
- /1/0/0
![1/0/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator1_0_0.png)
- /1/0/1
![1/0/1](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator1_0_1.png)
- /1/1/0
![1/1/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator1_1_0.png)
- /1/1/1
![1/1/1](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/mercator1_1_1.png)


### 地理投影的瓦片
- /0/0/0 
![0/0/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic0_0_0.png)
- /1/0/0
![1/0/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic1_0_0.png)
- /1/0/1
![1/0/1](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic1_0_1.png)
- /1/1/0
![1/1/0](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic1_1_0.png)
- /1/1/1
![1/1/1](https://github.com/zhuang-hao-ming/tms_research/blob/master/doc/img/geodetic1_1_1.png)

## raster
