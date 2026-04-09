#!/bin/bash
# 为 shownews.php 添加微信分享 API

FILE="/www/wwwroot/go.xiachaoqing.com/templates/epgo-education/shownews.php"

# 找到 </head> 或 <main> 前面，插入微信 SDK 和配置
# 我们插入在 <main> 标签之前（第2行之后）

WECHAT_CODE='<!-- 微信分享 API -->
<script src="https://res.wx.qq.com/open/js/jweixin-1.6.0.js"></script>
<script>
// 微信分享配置
document.addEventListener("DOMContentLoaded", function() {
    var title = document.querySelector("h1") ? document.querySelector("h1").innerText : document.title;
    var desc = "{$data.description}" || "英语陪跑 GO - 专业英语学习平台";
    var link = window.location.href;
    var imgUrl = "{$data.imgurl}" || "https://go.xiachaoqing.com/upload/logo.png";

    // 微信分享给好友
    wx.ready(function() {
        wx.shareAppMessage({
            title: title,
            desc: desc,
            link: link,
            imgUrl: imgUrl,
            type: "link",
            dataUrl: "",
            success: function() {
                console.log("分享给好友成功");
            },
            cancel: function() {
                console.log("取消分享");
            }
        });

        // 微信分享到朋友圈
        wx.onMenuShareTimeline({
            title: title,
            link: link,
            imgUrl: imgUrl,
            success: function() {
                console.log("分享到朋友圈成功");
            },
            cancel: function() {
                console.log("取消分享");
            }
        });
    });
});
</script>
'

# 在第 2 行之后（<include file="head.php" /> 之后）插入代码
sed -i '2a\'"$WECHAT_CODE" "$FILE"

echo "✅ 微信分享代码已集成到 $FILE"
