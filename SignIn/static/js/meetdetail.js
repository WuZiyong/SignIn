$(function () {


    //中文适配
    function utf16to8(str) {
        var out, i, len, c;
        out = "";
        len = str.length;
        for (i = 0; i < len; i++) {
            c = str.charCodeAt(i);
            if ((c >= 0x0001) && (c <= 0x007F)) {
                out += str.charAt(i);
            } else if (c > 0x07FF) {
                out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
                out += String.fromCharCode(0x80 | ((c >> 6) & 0x3F));
                out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
            } else {
                out += String.fromCharCode(0xC0 | ((c >> 6) & 0x1F));
                out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
            }
        }
        return out;
    }

    /**
     *  生成qrcode
     */
    function qrcode() {
        var url = $('.signin-url').attr('href');
        //var url = 'http://baidu.com';
        $('#qrcode').qrcode({
            render: "canvas", //也可以替换为table
            width: 150,
            height: 150,
            text: utf16to8(url)
        });
    }
    qrcode();


    /**
     *  点击事件 点击后下载签到名单
     */
    $('.downloadsignbutton').on('click', function () {
        var meet_uuid = $('#activitydetail').attr('meet');
        var meet_name = $('.meetname').attr('title');
        var type = 1;
        downloadfile(meet_uuid, meet_name, type)
    })
        
    /**
     *  点击事件 点击后下载缺勤名单
     */
     $('.downloadabsencebutton').on('click', function () {
        var meet_uuid = $('#activitydetail').attr('meet');
        var meet_name = $('.meetname').attr('title');
        var type = 2;
        downloadfile(meet_uuid, meet_name, type)
     })
    
    
    // 下载文件
    function downloadfile(meet_uuid, meet_name, type) {
        if (type == 1) {
            str = "签到";
        } else {
            str = "缺勤";
        }
        var index = layer.confirm('是否下载' + meet_name + "的"+str+"名单?", {
            btn: ['下载', '取消'], //按钮
            title: '提示'
        }, function () {
            console.log('下载' + meet_name + "的"+str+"名单");
            $.ajax({
                url: '/meet/download/?meet_uuid=' + meet_uuid+'&type='+type,
                type: 'GET',
            }).done(function () {
                creatLink(meet_uuid, type);
                layer.close(index);
                
            });
        }, function () {
            layer.close(index)
        });
    }


    // 临时创建下载链接
    function creatLink(meet_uuid,type) {
        var link = document.createElement('a');
        link.href = '/meet/download/?meet_uuid=' + meet_uuid+'&type='+type;
        link.setAttribute('download', '');
        link.dispatchEvent(new MouseEvent('click', {
            bubbles: true,
            cancelable: true,
            view: window
        }));
    }
        
})