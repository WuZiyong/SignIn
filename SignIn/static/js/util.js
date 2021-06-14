// =================================================================
//                         vvv 表单验证 vvv
// =================================================================
var formVerify = {
    /**
     * 必填字段验证，某字段没有填写时为其添加is-invalid类
     * @param $form jquery表单
     * @param requiredArray 必填字段名称
     * @returns {boolean} 通过验证返回true
     */
    requiredInput: function ($form, requiredArray) {
        if (!$.isArray(requiredArray)) {
            requiredArray = [requiredArray]
        }
        var result = true;
        requiredArray.forEach(function (required) {
            var $e = $form.find('[name=' + required + ']');
            if ($e.length != 0 && $.trim($e.val()) === '') {
                $e.addClass('is-invalid');
                $e.next().addClass('is-invalid'); // 一个时间输入会有两个input的情况(如移动端)
                result = false;
            }
        });
        // if (result == false) {
        //     $('.warningrow').append('<div class="alert alert-warning"></div>');
        // }
        return result;
    },

    /**
     * radio 表单验证
     * @param radioNames radio 名字 数组
     * @returns {boolean} 通过验证返回true
     */
    requiredRadio: function (radioName) {
        radioName.sort();
        $.unique(radioName);
        var result = true;
        $.each(radioName, function (i, val) {
            if ($("input[name=" + radioName + "]:checked").val() == null) {
                result = false;
            }
        });
        return result;
    }
};
// =================================================================
//                         ^^^ 表单验证 ^^^
// =================================================================

//给jQuery的form添加一个serializeObject，将表单内容转化为对象
(function ($) {
    $.fn.serializeObject = function () {
        "use strict";

        var result = {};
        var extend = function (i, element) {
            var node = result[element.name];

            if ('undefined' !== typeof node && node !== null) {
                if ($.isArray(node)) {
                    node.push(element.value);
                } else {
                    result[element.name] = [node, element.value];
                }
            } else {
                result[element.name] = element.value;
            }
        };

        $.each(this.serializeArray(), extend);
        return result;
    };
})(jQuery);

/**
 * 获取QueryStr
 * @returns {string}
 */
function getQueryStr() {
    return window.location.search.substring(1)
}

/**
 * 获取连接中的参数值
 * @param name
 * @returns {*}
 */

function getUrlParam(name) {
    return getParam(getQueryStr(), name)
}

/**
 * 获取参数
 * @param queryStr
 * @param name
 * @returns {*}
 */
var getParam = function getParam(queryStr, name) {
    var urlVariables = queryStr.split('&'), sParameterName

    for (var i = 0; i < urlVariables.length; i++) {
        sParameterName = urlVariables[i].split('=');

        if (sParameterName[0] === name) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};

