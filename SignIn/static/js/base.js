var url = document.URL;
var urls = url.split('/');
var url = urls[urls.length - 2];


function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

function timeTransfer(element) {
    var text;
    var time_list = document.getElementsByClassName(element)
    for (var i = 0; i < time_list.length; i++) {
        text = time_list[i].innerText;
        if (text == "None") {
            text = "未设置/未完成";
        } else {
            text = text.substring(5, 7) + '月' +
                text.substring(8, 10) + '日' +
                " " + text.substring(11, 16);
        }
        time_list[i].innerText = text;
        time_list[i].title = text;
    }
}

$(function () {
    // menubar 上当前页灰字变黑
    if (url == 'push') {
        // console.log(urls[urls.length - 2]);
        $("#active-push").addClass("active");
    } else if (url == 'push-history') {
        $("#active-history").addClass("active");
    } else if (url == 'push-new') {
        $("#active-push-new").addClass("active");
    } else if (url == 'homepage') {
        $("#active-homepage").addClass("active");
    } else {
        var selectID = "#active-" + getQueryString('select');
        // console.log(selectID);
        $(selectID).addClass("active");
        // if (select == 'photo')
    }
})


$(document).ready(function () {
    // =================================================================
    //                          页面显示优化
    // =================================================================
    var text, pre_text;
    // 时间显示优化
    var time_list = document.getElementsByClassName('time-content')
    var date_only_pre_text = new Array('DeadLine：', '计划发布日期：');
    for (var i = 0; i < time_list.length; i++) {
        text = time_list[i].innerText;
        pre_text = time_list[i].previousSibling.innerText;
        if (text == "None") {
            text = "未设置/未完成";
            // 未完成时候不显示完成时间
            if (pre_text === '完成时间：') {
                var will_delete = time_list[i].parentNode;
                will_delete.parentNode.removeChild(will_delete);
                // 删除节点后会动态删除数组内的节点，i 要往回一步
                i--;
                continue;
            }
        } else {
            text = text.substring(5, 7) + '月' +
                text.substring(8, 10) + '日' +
                " " + text.substring(11, 16);
            if (pre_text == '-') {
                text = text.substring(7, text.length);
            } else if (date_only_pre_text.indexOf(pre_text) != -1) {
                text = text.substring(0, 6);
            }
        }
        time_list[i].innerText = text;
    }
    timeTransfer('file-time');
})