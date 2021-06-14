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
     *  点击事件 生成活动
     */
     $('.signinbutton').on('click', function () {
        postnewtask()
    })


    /**
     * 
     * @param {} data 
     *  请求添加任务
     */
     function postnewtask() {
        $verify = $('#signinform');
        //表单验证
        //console.log(formVerify.requiredInput($verify,["meet_name","meet_begin_time","meet_end_time"]))
        
        if (formVerify.requiredInput($verify,["stu_name","stu_id"])) {
            var result = $verify.serializeObject();
            console.log(result);
            result['meet_uuid'] = $('#signin').attr('meet');
            var index = layer.confirm('姓名: '+result['stu_name']+' '+'学号: '+result['stu_id']+' 确认签到？', {
                btn: ['是', '否'], //按钮
                title: '提示'
            }, function () {
                $.ajax({
                    url: '/sign/newsign/',
                    type: 'POST',
                    data: result,
                }).done(function (response) {
                    layer.close(index);
                    // location.reload();
                    console.log('response.status: ',response.status)
                    if (response.status == 200) {
                        layer.msg(response.msg);
                    } else {
                        layer.msg(response.msg)
                    }
                });
            }, function () {
                layer.close(index)
            });
        }
        return false;
    }
})