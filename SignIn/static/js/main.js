$(function () {

    //========================实现应用页面跳转========================
    $('.createmeet').click(function () {
        window.location.href='/createmeet/';
    });
    $('.meetlist').click(function () {
        window.location.href='/main/#activitylist';
    });
    $('.setting').click(function () {
        window.location.href='/main/#setting';
    });


    //=========================活动列表有关函数===========================

    /**
     *  点击事件 点击进入详情页面
     */
    $('#meetlist tr').click(function () {
        meet_uuid = $(this).attr('meet');
        window.location.href = '/meetdetail/'+meet_uuid;
    });
    

    
    




    //========================实现设置页面上传文件===============================




    // 点击上传按钮
    $('#btnUpload').click(function () {
        $('#fileUpload').fileinput('upload');
    });


    /**
     * 上传控件
     * @param url
     * @param data
     * @param render
     * @constructor
     */
    function UploadWidget(url, data,render, extraSetting) {
        // 初始化控件
        var $fileUpload = $('#fileUpload');
        var setting = {
            language: 'zh',
            showPreview: false,
            showUpload: false,
            showCancel: false,
            showClose: false,
            showUploadedThumbs: false,
            browseIcon: '<i class="icon-folder-open"></i>',
            browseClass: 'btn-file-input btn-primary',
            browseLabel: '选择',
            removeIcon: '<i class="icon-trash"></i>',
            removeLabel: '删除',
            removeClass: 'btn-file-input btn-secondary',
            removeTitle: '删除文件',
            uploadAsync: false,
            showAjaxErrorDetails: false,
            //allowedFileTypes:["xls"],//'csv','xls',
            allowedFileExtensions:["xls","csv","xlsx"],
            elErrorContainer: '#fileError',
            minFileCount: 1,
            maxFileSize: 10240, //需配合服务端一起改
            uploadUrl: url,
            uploadExtraData: data,
        };
        Object.assign(setting, extraSetting);
        $fileUpload.fileinput(setting).on('change', function (event) {
            $('#btnUpload').removeAttr('disabled');
        }).on('fileclear', function (event) {
            $('#btnUpload').attr('disabled', 'disabled');
        }).on('fileerror', function (event, data, msg) {
            console.log(msg);
        }).on('filebatchuploadsuccess', function (event, data) {
            var response = data.response;
            console.log(response);
            $fileUpload.fileinput('unlock').fileinput('clear');
            $('.modal').modal('hide');
            render(data)
        });

        // 注册唤醒modal后清空事件
        $('.modal').on('show.bs.modal', function (e) {
            $fileUpload.fileinput('clear');
        });
    }


    /**
     * 上传文件+上传控件
     */

    $('.uploadfilebutton').on('click',function () {
        var url = '/resource/upload';
        var grade = $('.settingselect').find('option:selected').attr('value');
        var data = {
            'grade':grade,
        }
        $('#fileUpload').fileinput('destroy');
        UploadWidget(url, data, UploadRender, {});
    })
    

    function UploadRender(data) {
        var response = data.response;
        if (response.status === 200) {
            //var files = response.files;
            //add_file_icon(files);
            layer.msg(response.msg);
        } else {
            console.log(response.msg);
            $("#fileUpload").fileinput('clear');
        }

    }


    /**
     *  下载文件
     */

    $('.downloadfilebutton').on("click", function () {
        $fileHistory = $(this).closest('.file-history')
        var grade = $('.settingselect').find('option:selected').attr('value');
        var grade_zh = $('.settingselect').find('option:selected').text()
        var index = layer.confirm('是否下载' + grade_zh + "的名单?", {
            btn: ['下载', '取消'], //按钮
            title: '提示'
        }, function () {
            console.log('下载：' + grade_zh +'名单');
            $.ajax({
                url: '/resource/download/' + grade,
                type: 'GET',
            }).done(function () {
                creatLink(grade);
                layer.close(index)
            });
        }, function () {
            layer.close(index)
        });
    });
    // 临时创建下载链接
    function creatLink(grade) {
        var link = document.createElement('a');
        link.href = '/resource/download/' + grade;
        link.setAttribute('download', '');
        link.dispatchEvent(new MouseEvent('click', {
            bubbles: true,
            cancelable: true,
            view: window
        }));
    }

    /**
     *  删除文件
     */

    $('.container').on("click", '.icon-remove', function () {
        $fileHistory = $(this).closest('.file-history')
        var file_name = $fileHistory.attr('file_name')
        var resource_uuid = $fileHistory.attr('resource_uuid');
        var index = layer.confirm('是否删除文件「' + file_name + "」?", {
            btn: ['删除', '取消'], //按钮
            title: '提示'
        }, function () {
            console.log('删除：' + resource_uuid);
            $.ajax({
                url: '/resource/delete/' + resource_uuid,
                type: 'GET',
            }).done(function (response) {
                layer.close(index)
                layer.msg(response.msg)
                $fileHistory.remove()
            });
        }, function () {
            layer.close(index)
        });
    });











})