const backgroundData = [
    {
        image: './assets/images/background/bg2.jpg',
        chinese_title: '抚远 · 东极广场',
        english_title: 'East Polar Plaza, Fuyuan, China',
        pic_date: '摄于2025年1月1日 Pictured at Jan. 1st, 2025'
    },
    {
        image: './assets/images/background/bg1.jpg',
        chinese_title: '富锦 · 001乡道',
        english_title: 'Village Road 001, Fujin, China',
        pic_date: '摄于2025年1月1日 Pictured at Jan. 1st, 2025'
    },
    {
        image: './assets/images/background/bg3.jpg',
        chinese_title: '富锦 · 锦山 <span style="font-size:0.5em">（别拉音子山）</span>',
        english_title: 'Jinshan Hill <span style="font-size:0.5em">(Bielayin Hill)</span>, Fujin, China',
        pic_date: '摄于2024年12月31日 Pictured at Dec. 31st, 2024'
    },
    {
        image: './assets/images/background/bg4.jpg',
        chinese_title: '延庆 · 野鸭湖国家湿地公园',
        english_title: 'Yeyahu National Wetland Park, Yanqing, China',
        pic_date: '摄于2024年12月3日 Pictured at Dec. 3rd, 2024'
    },
    {
        image: './assets/images/background/bg5.jpeg',
        chinese_title: '柏林 · 苏军纪念碑',
        english_title: 'Sowjetisches Ehrenmal, Berlin, Deutschland<br/>Soviet War Memorial, Berlin, Germany',
        pic_date: '摄于2024年11月16日 Pictured at Nov. 16th, 2024'
    },   
    {
        image: './assets/images/background/bg6.jpg',
        chinese_title: '柏林 · 奥伯鲍姆桥',
        english_title: '<span style="font-size:80%;">Oberbaumbrüke, Berlin, Deutschland<br/>Oberbaum Bridge, Berlin, Germany</span>',
        pic_date: '<span style="font-size:90%;">摄于2024年11月16日 Pictured at Nov. 16th, 2024</span>'
    },    
    
    // 暗色图片专用样式
    {
        image: './assets/images/background/bg7.jpg',
        chinese_title: '<span style="color: var(--bs-gray-400);">南昌 · 赣江两岸</span>',
        english_title: '<span style="color: var(--bs-gray-400);">Two Sides of the Ganjiang river</span>',
        pic_date: '<span style="color: var(--bs-gray-400);">摄于2025年2月5日 Pictured at Feb. 5th, 2025</span>'
    },    
];

// const backgroundData = [
//     {
//         image: './assets/images/background/special_day.jpeg',
//         chinese_title: '<span style="color: var(--bs-gray-400);">你怎么知道我给我对象450抽出了9个金？</span>',
//         english_title: '<span style="color: var(--bs-gray-400);">How did you know I got 9 golds in 450 pulls for my GF?</span>',
//         pic_date: '<span style="color: var(--bs-gray-400);">于2025年3月4日  At Mar. 4th, 2025</span>'
//     },
// ];

function preloadImages() {
    backgroundData.forEach(item => {
        const img = new Image();
        img.src = item.image;
    });
}

function initCarousel() {

    preloadImages(); // 预加载图片

    let currentCarousel = document.querySelector('.background-carousel');
    let currentCaption = document.querySelector('.caption-container');
    let currentIndex = 0;
    let zIndexCounter = 1;

    function createNewSlide(index) {
        // 创建新背景容器
        const newCarousel = document.createElement('div');
        newCarousel.className = 'background-carousel';
        newCarousel.style.backgroundImage = `url(${backgroundData[index].image})`;
        newCarousel.style.zIndex = zIndexCounter;
        newCarousel.style.opacity = 0;

        // 创建新文字容器
        const newCaption = document.createElement('div');
        newCaption.className = 'caption-container';
        newCaption.style.zIndex = zIndexCounter + 1;
        newCaption.style.opacity = 0;
        newCaption.innerHTML = `
            <div class="container px-4 px-lg-5">
                <div class="row gx-4 gx-lg-5">
                    <div class="col-lg-10">
                        <h1 class="mt-5 chinese_title">${backgroundData[index].chinese_title}</h1>
                        <h1 class="mt-0-mainpage-title english_title">${backgroundData[index].english_title}</h1>
                        <p class="pic_date">${backgroundData[index].pic_date}</p>
                    </div>
                </div>
            </div>
        `;

        return { newCarousel, newCaption };
    }

    function changeBackground() {
        // 生成新索引（确保不重复）
        let newIndex;
        do {
            newIndex = Math.floor(Math.random() * backgroundData.length);
        } while (backgroundData.length > 1 && newIndex === currentIndex);

        // 创建新幻灯片
        const { newCarousel, newCaption } = createNewSlide(newIndex);
        document.body.appendChild(newCarousel);
        document.body.appendChild(newCaption);

        // 触发过渡动画
        requestAnimationFrame(() => {
            newCarousel.style.opacity = 1;
            newCaption.style.opacity = 1;
            
            // 隐藏旧幻灯片
            if (currentCarousel) {
                currentCarousel.style.opacity = 0;
            }
            if (currentCaption) {
                currentCaption.style.opacity = 0;
            }
        });

        // 延迟移除旧元素
        setTimeout(() => {
            currentCarousel?.remove();
            currentCaption?.remove();
            
            // 更新当前引用
            currentCarousel = newCarousel;
            currentCaption = newCaption;
            currentIndex = newIndex;
            zIndexCounter += 2;
        }, 1000); // 匹配CSS过渡时间
    }

    // 初始化首屏
    // 初始化首屏（新增文字内容填充）
    currentCarousel.style.backgroundImage = `url(${backgroundData[currentIndex].image})`;
    currentCaption.innerHTML = `
        <div class="container px-4 px-lg-5">
            <div class="row gx-4 gx-lg-5">
                <div class="col-lg-10">
                    <h1 class="mt-5 chinese_title">${backgroundData[currentIndex].chinese_title}</h1>
                    <h1 class="mt-0-mainpage-title english_title">${backgroundData[currentIndex].english_title}</h1>
                    <p class="pic_date">${backgroundData[currentIndex].pic_date}</p>
                </div>
            </div>
        </div>
    `;
    currentCarousel.style.opacity = 1;
    currentCaption.style.opacity = 1;

    // 设置轮播间隔（建议5秒）
    setInterval(changeBackground, 86400*1000);
}

document.addEventListener('DOMContentLoaded', initCarousel);
