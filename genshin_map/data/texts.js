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
      description: "支持局部字号、颜色与换行。",
      location: "富文本示例",
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
  }
];
