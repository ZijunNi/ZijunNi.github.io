window.markers = [
  {
    id: "great_wall",
    name: "八达岭长城",
    level: 3,
    x: 1220, y: 1584, // 图标位置（像素坐标）
    icon: {
      // 方式1：图片图标（png/svg/jpg）。如果你有 marker.png 放同目录，可启用：
      url: "./assets/great_wall.png",
      size: [68.3, 54.5],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [34.15, 28.25]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）

      // 方式2：divIcon（不依赖图片）——默认使用这个保证可运行
      // divIcon: true,
      // html: `<div style="
      //   width:18px;height:18px;border-radius:999px;
      //   background:#111;border:3px solid #fff;
      //   box-shadow:0 6px 14px rgba(0,0,0,0.25);
      // "></div>`,
      // size: [18, 18],
      // anchor: [9, 9]
    },
    info: { type: "Marker", description: "示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）", tags: ["demo"], updatedAt: "2026-01-08" }
  },

  {
    id: "beijing",
    name: "北京",
    level: 1,
    x: 1314, y: 1453,
    icon: {
      url: "./assets/city_center.png",
      size: [52.2, 80.5],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [26.1, 80.5]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）
    },
    info: { type: "Marker", description: "北倚燕山余脉，西承太行屏障，南向华北平原徐徐铺展，北京安坐于山川收束与大地开阔的交界处，大自然在此设下经略四方的格局。\n 城市中轴线如一条缓缓展开的时间之线，自紫禁城的屋脊延伸至天安门广场的开阔空间，王朝的秩序与时代的叙事在此交汇；未名湖畔，燕园静立，书声在林影与旧楼之间回荡，思想悄然生长；远望城郊，群山起伏，古关与驿道隐没在岁月之中，静静诉说往昔。山河依旧、人事却不断更替，这座城市究竟是在被时间塑造，还是在与时间对话？", tags: ["info","panel"], updatedAt: "2026-01-08", location: "北京市" }
  },

  {
    id: "baoding",
    name: "保定",
    level: 1,
    x: 1128, y: 1064,
    icon: {
      url: "./assets/city_center.png",
      size: [52.2, 80.5],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [26.1, 80.5]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）
    },
    info: { type: "Marker", description: "示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）", tags: ["info","panel"], updatedAt: "2026-01-08" }
  },

    {
    id: "langfang",
    name: "廊坊",
    level: 1,
    x: 1435, y: 1320,
    icon: {
      url: "./assets/city_center.png",
      size: [52.2, 80.5],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [26.1, 80.5]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）
    },
    info: { type: "Marker", description: "示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）", tags: ["info","panel"], updatedAt: "2026-01-08" }
  },


    {
    id: "tianjin",
    name: "天津",
    level: 1,
    x: 1569, y: 1218,
    icon: {
      url: "./assets/city_center.png",
      size: [52.2, 80.5],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [26.1, 80.5]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）
    },
    info: { type: "Marker", description: "示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）", tags: ["info","panel"], updatedAt: "2026-01-08" }
  },


  {
    id: "zhangjiakou",
    name: "张家口",
    level: 1,
    x: 904, y: 1738,
    icon: {
      url: "./assets/city_center.png",
      size: [52.2, 80.5],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [26.1, 80.5]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）
    },
    info: { type: "Marker", description: "示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）示例标记点 B（点击查看侧边栏）", tags: ["info","panel"], updatedAt: "2026-01-08" }
  }


];
