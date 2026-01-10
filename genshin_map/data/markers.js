window.markers = [
  {
    id: "m1",
    name: "八达岭长城",
    level: 2,
    x: 1220, y: 1584,
    icon: {
      // 方式1：图片图标（png/svg/jpg）。如果你有 marker.png 放同目录，可启用：
      url: "./assets/great_wall.png",
      size: [68.3, 54.5],  // 显示在地图中的图标尺寸（像素，注意等比例缩放）
      anchor: [34.15, 28.25]

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
    info: { type: "Marker", description: "示例标记点 A（坐标：像素）", tags: ["demo"], updatedAt: "2026-01-08" }
  },
  {
    id: "m2",
    name: "Point B",
    level: 2,
    x: 1200, y: 650,
    icon: {
      divIcon: true,
      html: `<div style="
        width:18px;height:18px;border-radius:6px;
        background:#0b57d0;border:3px solid #fff;
        box-shadow:0 6px 14px rgba(0,0,0,0.25);
      "></div>`,
      size: [18, 18],
      anchor: [9, 9]
    },
    info: { type: "Marker", description: "示例标记点 B（点击查看侧边栏）", tags: ["info","panel"], updatedAt: "2026-01-08" }
  }
];
