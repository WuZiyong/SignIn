// =================================
//            干事多人模式
// =================================
$(function () {
    // 添加成员模板
    var tmplAddMember = '<span class="multi-workers"><span class="name">${name}</span><span class="delete-member">×</span></span>'
    $.template("addMember", tmplAddMember);
    // 添加成员
    $('.member-add').on('click', function (e) {
        e.preventDefault();
        var $input = $(this).prev();
        // var a = $(this).parent().prev().children()[0];
        var val = $input.val();
        var msg = '请先填写人员姓名😲';
        if ($.trim($input.val()) === '') {
            $input.addClass('is-invalid');
            $(".alert-warning").removeClass('d-n').text(msg);
        } else {
            $.tmpl("addMember", { "name": val }).appendTo($(this).parent().prev())
            // 输入栏清空
            $input.val('');
            // 影藏警告文字
            if ($('.alert').text() == msg) {
                $('.alert').addClass('d-n');
            }
        }
    })
    // 删除成员
    $('.members-all').on('click', '.delete-member', function () {
        $(this).parent().remove();
    })
    // 确认键
    $('.btn-ok').on('click', function (e) {
        e.preventDefault();
        $(this).parent().next().children()[0].value = $(this).prev().text();
        $(this).prev().text('');
        $(this).parent().addClass('d-n');
    })
    // 输入框内容监听：用于消除 is-invalid
    $(".form-control").bind('input propertychange', function () {
        if ($(this).hasClass('is-invalid') && $.trim($(this).val()) != '') {
            $(this).removeClass('is-invalid');
        }
    })
})