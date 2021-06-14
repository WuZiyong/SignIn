$(function () {
    /** 
     *  生成活动 checkbox 选中全院/本科生/研究生 实现 
     */
     $('.checkall').on('click',function () {
        if ($(this).is(':checked')) {
            $('.checkunder').prop("checked", true);
            $('.checkgrad').prop("checked", true);
        } else {
            $('.checkunder').prop("checked", false);
            $('.checkgrad').prop("checked", false);
            $('.checkundergraduate').prop("checked", false);
            $('.checkgraduate').prop("checked", false);
        }
    })
    $('.checkundergraduate').on('click',function () {
        if ($(this).is(':checked')) {
            $('.checkunder').prop("checked", true);
        } else {
            $('.checkunder').prop("checked", false);
        }
    })
    $('.checkgraduate').on('click',function () {
        if ($(this).is(':checked')) {
            $('.checkgrad').prop("checked", true);
        } else {
            $('.checkgrad').prop("checked",false);
        }
    })
    $('.checkunder').on('click',function () {
        if (!$(this).is(':checked')) {
            $('.checkundergraduate').prop("checked", false);
            $('.checkall').prop("checked", false);
        }
    })
    $('.checkgrad').on('click',function () {
        if (!$(this).is(':checked')) {
            $('.checkgraduate').prop("checked", false);
            $('.checkall').prop("checked", false);
        }
    })


        //=======================实现生成活动页面===============================


    /**
     *  点击事件 生成活动
     */
     $('.createactbutton').on('click', function () {
        postnewtask()
    })


    /**
     * 
     * @param {} data 
     *  请求添加任务
     */
     function postnewtask() {
        $verify = $('#createactivityform');
        //表单验证
        //console.log(formVerify.requiredInput($verify,["meet_name","meet_begin_time","meet_end_time"]))
        
        if (formVerify.requiredInput($verify,["meet_name","meet_begin_time","meet_end_time"])) {
            var result = $verify.serializeObject();
            console.log(result)
            if (result['need_grade'] instanceof Array) {
                result['new_need_grade'] = result['need_grade'].join('')
            } else {
                result['new_need_grade'] = result['need_grade']
            }
            var index = layer.confirm('是否生成活动'+result['meet_theme']+':'+result['meet_name']+'？*注意(超过结束时间学生将无法签到,请谨慎输入)', {
                btn: ['是', '否'], //按钮
                title: '提示'
            }, function () {
                $.ajax({
                    url: '/sign/newmeet/',
                    type: 'POST',
                    data: result,
                }).done(function (response) {
                    layer.close(index);
                    // location.reload();
                    console.log('response.status: ',response.status)
                    if (response.status == 200) {
                        layer.msg('提交完成');
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