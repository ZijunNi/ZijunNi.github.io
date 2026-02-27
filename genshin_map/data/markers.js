// 标记分级显示规则（文字和图表均按此规则）
//   { level: 1, minZoom: 0 }, // 目前未启用的层级
//   { level: 2, minZoom: 1 }, // 目前未启用的层级
//   { level: 3, minZoom: 2 }, // 目前未启用的层级
//   { level: 4, minZoom: 3 }, // 目前未启用的层级
//   { level: 5, minZoom: 4 }, // 仅显示省级地名的层级
//   { level: 6, minZoom: 5 }, // 地级区域中心神像对应的层级，此级别(4.5以下)开始省级地名不显示
//   { level: 7, minZoom: 6 }, // 地级区域文字、传送锚点显示对应的层级
//   { level: 8, minZoom: 7 }, // 重要景点对应的层级
//   { level: 9, minZoom: 8 }

window.markers = [

// ******************* 景点 *******************
  {
    id: "great_wall",
    name: "八达岭长城",
    level: 3, // 最大显示层级数+1，低于这个层级才会显示
    x: 13408, y: 11594, // 图标位置（像素坐标）
    min_zoom: 7,   // 可选：最小显示缩放
    icon: {
      // 方式1：图片图标（png/svg/jpg）。如果你有 marker.png 放同目录，可启用：
      url: "./assets/great_wall.png",
      size: [34, 27],  // 显示在地图中的图标尺寸（像素，注意等比例缩放，参考大小30x30）
      anchor: [17, 13.5]// 图标锚点
      // （图标左上角为[0,0]，锚点位置决定图标的定位点，对于30x30的图标，下边缘中点作为锚点时应为[15, 30]）

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
    info: { 
      type: "Marker", 
      location: "北京市 · 延庆区" ,
      description: "示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）示例标记点 A（坐标：像素）", 
      // 可选：侧边栏描述下方图片（建议放在 ./assets/photos/ 下）
      // photo: "./assets/photos/badaling.jpg",
      // 可选：图片 alt 文本
      // photoAlt: "八达岭长城",
      tags: ["demo"], 
      updatedAt: "2026-01-08"
    }
  },
  {
    id: "yunshifuzhong",
    name: "云师附中",
    level: 8,
    x: 9465, y: 7129, // 图标位置（像素坐标）
    min_zoom: 7,   // 可选：最小显示缩放
    icon: {
      url: "./assets/yunshifuzhong.png",
      size: [33.08, 28.8],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [16.54, 28.8]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）
    },
    info: { type: "Marker", description: "占位符", tags: ["demo"], updatedAt: "2026-01-08", location: "昆明市 · 五华区"  }
  },

// ******************* 地级中心 *******************

  {
    id: "beijing",
    name: "北京",
    level: 1,
    x: 13489, y: 11473,
    min_zoom: 5,   // 可选：最小显示缩放
    // max_zoom: 9,   // 可选：最大显示缩放
    icon: {
      url: "./assets/city_center.png",
      size: [26.1, 40.25],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [13.05, 40.25]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）
    },
    info: { type: "Marker", description: "北倚燕山余脉，西承太行屏障，南向华北平原徐徐铺展，北京安坐于山川收束与大地开阔的交界处，大自然在此设下经略四方的格局。\n 城市中轴线如一条缓缓展开的时间之线，自紫禁城的屋脊延伸至天安门广场的开阔空间，王朝的秩序与时代的叙事在此交汇；未名湖畔，燕园静立，书声在林影与旧楼之间回荡，思想悄然生长；远望城郊，群山起伏，古关与驿道隐没在岁月之中，静静诉说往昔。山河依旧、人事却不断更替，这座城市究竟是在被时间塑造，还是在与时间对话？", tags: ["info","panel"], updatedAt: "2026-01-08", location: "北京市" }
  },

  {
    id: "dali",
    name: "大理",
    level: 1,
    x: 8765, y: 7275,
    min_zoom: 5,   // 可选：最小显示缩放
    max_zoom: 9,   // 可选：最大显示缩放
    icon: {
      url: "./assets/city_center.png",
      size: [26.1, 40.25],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [13.05, 40.25]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）
    },
    info: { type: "Marker", 
      description: "西枕苍山巍峨，东浮洱海烟波，南望佛国钟磬，北依古道遗风，大理坐落于苍洱坝子的暖阳之中。\n 苍山巍峨如屏，拱卫着千载古城的烟火人间；洱海澄波似镜，倒映出三塔凌空的清寂倒影。崇圣寺钟声随风远播，诉说着妙香古国的慈悲与安宁；喜洲古城的稻浪深处，白族照壁静静伫立，刻写下耕读传家的古风。千年的“风花雪月”，正静待旅者的探索。", 
      tags: ["info","panel"], 
      updatedAt: "2026-01-08", 
      photo: "./assets/photos/dali.jpg",
      location: "云南省 · 大理市"  }
  },
    {
    id: "kunming",
    name: "昆明",
    level: 5,
    x: 9525, y: 7065,
    min_zoom: 5,   // 可选：最小显示缩放
    max_zoom: 9,   // 可选：最大显示缩放
    icon: {
      url: "./assets/city_center.png",
      size: [26.1, 40.25],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [13.05, 40.25]// 图标锚点（图标左上角为[0,0]，锚点位置决定图标的定位点）
    },
    info: { 
      type: "Marker", 
      description: "南拥滇池烟波，东枕金马晴岚，西倚碧鸡苍翠，北收乌蒙余势，昆明坐落于高原台地与湖泊襟怀之间。\n翠湖波光如散落的旧笺，海鸥年年衔来远方的消息，讲武堂的黄墙沉默伫立，共和的初啼曾在此划破晨雾；河山破碎之际，西南联大在春城留下足迹，保留下文明的火种；海晏河清之时，云师附中于故地续写弦歌，传扬着先贤的薪火。春城昆明，向每一位旅者敞开怀抱。", 
      tags: ["info","panel"], 
      updatedAt: "2026-01-08", 
      location: "云南省 · 昆明市"  
    }
  }

];
