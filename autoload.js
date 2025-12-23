/*!
 * Live2D Widget - 私有修改版
 * 自动适配 window.live2d_path
 */

// 1. 自动检测资源路径：如果油猴脚本定义了路径就用脚本的，否则尝试自动定位
if (typeof live2d_path === 'undefined') {
    // 默认回退机制，防止报错
    var live2d_path = "";
    var scripts = document.getElementsByTagName('script');
    var script = scripts[scripts.length - 1];
    if (script.src.indexOf('autoload.js') > -1) {
        live2d_path = script.src.replace('autoload.js', '');
    }
}

// 2. 封装加载函数
function loadExternalResource(url, type) {
    return new Promise((resolve, reject) => {
        let tag;
        if (type === 'css') {
            tag = document.createElement('link');
            tag.rel = 'stylesheet';
            tag.href = url;
        } else if (type === 'js') {
            tag = document.createElement('script');
            tag.type = 'module';
            tag.src = url;
        }
        if (tag) {
            tag.onload = () => resolve(url);
            tag.onerror = () => reject(url);
            document.head.appendChild(tag);
        }
    });
}

// 3. 核心加载逻辑
(async () => {
    // 手机端判断 (可选，这里先注释掉，由油猴脚本控制)
    // if (screen.width < 768) return;

    // 解决图片跨域
    const OriginalImage = window.Image;
    window.Image = function(...args) {
        const img = new OriginalImage(...args);
        img.crossOrigin = "anonymous";
        return img;
    };
    window.Image.prototype = OriginalImage.prototype;

    // 加载 CSS 和 核心逻辑 JS
    // 注意：这里我们强制它去 live2d_path 加载，而不是去 npm
    await Promise.all([
        loadExternalResource(live2d_path + 'waifu.css', 'css'),
        loadExternalResource(live2d_path + 'waifu-tips.js', 'js')
    ]);

    // 读取油猴脚本设置的配置
    const settings = window.live2d_settings || {};

    // 初始化看板娘
    initWidget({
        waifuPath: settings.waifuPath || live2d_path + 'waifu-tips.json',
        cdnPath: settings.cdnPath || live2d_path, // 模型根目录
        tools: settings.tools || ['hitokoto', 'asteroids', 'switch-model', 'switch-texture', 'photo', 'info', 'quit'],
        drag: settings.waifuDraggable !== 'disable',
        logLevel: 'warn'
    });
})();

console.log(`Live2D 加载自: ${live2d_path}`);
