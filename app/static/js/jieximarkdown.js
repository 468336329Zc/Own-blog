
<!--markdown-comment是存放在id等于markdown-comment的markdown文档!-->
editormd.markdownToHTML("markdown-comment", {

            htmlDecode: "style,script,iframe", //可以过滤标签解码
            emoji: true,
            codefold: true,
            taskList: true,
            tex: true,               // 默认不解析
            flowChart: true,         // 开启流程图不解析
            sequenceDiagram: true,//开启时序/序列图支持，默认关闭,
            syncScrolling: "single",
            imageUpload: true,
            imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
            imageUploadURL: "./php/upload.php",
            onload: function () {
                console.log('onload', this);
                this.height(480);
            }});


    function popDown(){
        pop.className = 'modal';
        flag = 0;
        console.log(1);
    }

