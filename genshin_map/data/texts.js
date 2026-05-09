window.texts = [
  // {
  //   id: "text-1",
  //   name: "京津冀地区",
  //   text: "京津冀地区\n 探索度 10\% ",
  //   level: 1,
  //   x: 13430, y: 11016,
  //   min_zoom: 1,   // 可选：最小显示缩放
  //   max_zoom: 7,   // 可选：最大显示缩放
  //   // 可选：侧边栏图标（若不填则隐藏）
  //   // icon: {
  //   //   url: "./assets/city_center.png",
  //   //   size: [28, 28],
  //   //   anchor: [14, 14]
  //   // },
  //   info: {
  //     description: "这是一个文字模块示例。可用于地名、区域说明或剧情提示。",
  //     location: "京津冀地区"
  //   }
  // },
  {
    id: "jingjinji",
    name: "京津冀地区",
    level: 1,
    x: 13430, y: 11016,
    min_zoom: 1,   // 可选：最小显示缩放
    max_zoom: 4.5,   // 可选：最大显示缩放
    rich_text: [
      { text: "京津冀地区", size: 28, color: "#ffffff" },
      { br: true },
      { text: "探索度 ", size: 16, color: "#ffffff" },
      { text: "28%", size: 16, color: "#ffffff" }
    ],
    info: {
      description: "位于中国北方腹地，北靠蒙古高原，南望华北平原，东临渤海。",
      location: "京津冀地区",
      // 可选：侧边栏描述下方图片（建议放在 ./assets/photos/ 下）
      // photo: "./assets/photos/jingjinji.jpg",
      // 可选：图片 alt 文本
      // photoAlt: "京津冀地区示意图"
    }
  },
  {
    id: "shanxi",
    name: "山西省",
    level: 1,
    x: 12478, y: 10902,
    min_zoom: 1,   // 可选：最小显示缩放
    max_zoom: 4.5,   // 可选：最大显示缩放
    rich_text: [
      { text: "山西省", size: 28, color: "#ffffff" },
      { br: true },
      { text: "探索度 ", size: 16, color: "#ffffff" },
      { text: "9%", size: 16, color: "#ffffff" }
    ],
    info: {
      description: "占位符",
      location: "山西省",
      // 可选：侧边栏描述下方图片（建议放在 ./assets/photos/ 下）
      // photo: "./assets/photos/jingjinji.jpg",
      // 可选：图片 alt 文本
      // photoAlt: "京津冀地区示意图"
    }
  },
  {
    id: "henan",
    name: "河南省",
    level: 1,
    x: 12678, y: 9650,
    min_zoom: 1,   // 可选：最小显示缩放
    max_zoom: 4.5,   // 可选：最大显示缩放
    rich_text: [
      { text: "河南省", size: 28, color: "#ffffff" },
      { br: true },
      { text: "探索度 ", size: 16, color: "#ffffff" },
      { text: "9%", size: 16, color: "#ffffff" }
    ],
    info: {
      description: "占位符",
      location: "河南省",
      // 可选：侧边栏描述下方图片（建议放在 ./assets/photos/ 下）
      // photo: "./assets/photos/jingjinji.jpg",
      // 可选：图片 alt 文本
      // photoAlt: "京津冀地区示意图"
    }
  },
  {
    id: "yunnan",
    name: "云南省",
    level: 1,
    x: 9040, y: 6900,
    min_zoom: 1,   // 可选：最小显示缩放
    max_zoom: 4.5,   // 可选：最大显示缩放
    rich_text: [
      { text: "云南省", size: 28, color: "#ffffff" },
      { br: true },
      { text: "探索度 ", size: 16, color: "#ffffff" },
      { text: "13%", size: 16, color: "#ffffff" }
    ],
    info: {
      description: "位于中国西南边陲，西北枕着世界屋脊青藏高原，东南紧邻热带与亚热带平原丘陵的省份。过渡地带的地理位置，造就了“一山隔四季，十里不同天”的跌宕地貌。层叠的山峦与幽深的峡谷之间，复杂的地貌孕育出丰富的气候与生态，为万千生灵提供了栖居的家园。这片土地也因此成为自然与文明的交汇之所，多元的民族文化在此繁茂生长。",
      location: "云南省",
      // photo: "./assets/photos/yunnan.jpg",
      // photoAlt: "云南省风景"
    }
  },

  {
    id: "hubei",
    name: "湖北省",
    level: 1,
    x: 12804, y: 8639,
    min_zoom: 1,   // 可选：最小显示缩放
    max_zoom: 4.5,   // 可选：最大显示缩放
    rich_text: [
      { text: "湖北省", size: 28, color: "#ffffff" },
      { br: true },
      { text: "探索度 ", size: 16, color: "#ffffff" },
      { text: "10%", size: 16, color: "#ffffff" }
    ],
    info: {
      description: "位于中国腹地正中。",
      location: "湖北省",
      // photo: "./assets/photos/yunnan.jpg",
      // photoAlt: "云南省风景"
    }
  },

  {
    id: "jiangxi",
    name: "江西省",
    level: 1,
    x: 13639, y: 8109,
    min_zoom: 1,   // 可选：最小显示缩放
    max_zoom: 4.5,   // 可选：最大显示缩放
    rich_text: [
      { text: "江西省", size: 28, color: "#ffffff" },
      { br: true },
      { text: "探索度 ", size: 16, color: "#ffffff" },
      { text: "8%", size: 16, color: "#ffffff" }
    ],
    info: {
      description: "位于中国腹地正中。",
      location: "江西省",
      // photo: "./assets/photos/yunnan.jpg",
      // photoAlt: "云南省风景"
    }
  },

  {
    id: "anhui",
    name: "安徽省",
    level: 1,
    x: 13813, y: 9074,
    min_zoom: 1,   // 可选：最小显示缩放
    max_zoom: 4.5,   // 可选：最大显示缩放
    rich_text: [
      { text: "安徽省", size: 28, color: "#ffffff" },
      { br: true },
      { text: "探索度 ", size: 16, color: "#ffffff" },
      { text: "8%", size: 16, color: "#ffffff" }
    ],
    info: {
      description: "位于中国腹地正中。",
      location: "江西省",
      // photo: "./assets/photos/yunnan.jpg",
      // photoAlt: "云南省风景"
    }
  },

  {
    id: "heilongjiang",
    name: "黑龙江省",
    level: 1,
    x: 17091, y: 13300,
    min_zoom: 1,   // 可选：最小显示缩放
    max_zoom: 4.5,   // 可选：最大显示缩放
    rich_text: [
      { text: "黑龙江省", size: 28, color: "#ffffff" },
      { br: true },
      { text: "探索度 ", size: 16, color: "#ffffff" },
      { text: "19%", size: 16, color: "#ffffff" }
    ],
    info: {
      description: "位于中国东北边陲，是中国最靠东和北的省份。",
      location: "黑龙江省",
      // photo: "./assets/photos/yunnan.jpg",
      // photoAlt: "云南省风景"
    }
  },

  {
    id: "jiangzhehu",
    name: "江浙沪地区",
    level: 1,
    x: 14776, y: 8800,
    min_zoom: 1,   // 可选：最小显示缩放
    max_zoom: 4.5,   // 可选：最大显示缩放
    rich_text: [
      { text: "江浙沪地区", size: 28, color: "#ffffff" },
      { br: true },
      { text: "探索度 ", size: 16, color: "#ffffff" },
      { text: "3%", size: 16, color: "#ffffff" }
    ],
    info: {
      description: "位于中国东部沿海，是中国经济最发达的地区之一。",
      location: "江浙沪地区",
      // photo: "./assets/photos/yunnan.jpg",
      // photoAlt: "云南省风景"
    }
  }


];
