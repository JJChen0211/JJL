// // 窗口加载事件仅用于窗口高度取决于图像
// $(window).bind("load", function() {
//     var footerHeight = 0,
//     footerTop = 0,
//     $footer = $("#footer");
//     positionFooter();
// 　　//定义positionFooter function
// 　　function positionFooter() {
// 　　//取到div#footer高度
// 　footerHeight = $footer.height();
// 　 //div#footer离屏幕顶部的距离
// 　　footerTop = ($(window).scrollTop()+$(window).height()-footerHeight)+"px";
// 　　/* DEBUGGING STUFF
// 　　console.log("Document height: ", $(document.body).height());
// 　　console.log("Window height: ", $(window).height());
// 　 console.log("Window scroll: ", $(window).scrollTop());
// 　　console.log("Footer height: ", footerHeight);
// 　　console.log("Footer top: ", footerTop);
// 　　console.log("-----------")
// 　　*/
// 　　//如果页面内容高度小于屏幕高度，div#footer将绝对定位到屏幕底部，否则div#footer保留它的正常静态定位
// 　　　　if ( ($(document.body).height()+footerHeight) < $(window).height()) {
//    　　 $footer.css({
//        　　 position: "absolute"
//    　　 }).stop().animate({
//        　　 top: footerTop
//    　　 });
// 　　　 }else {
//    　　　　 $footer.css({
//        　　 position: "static"
//     　　　　});
// 　　　　}
// 　　}
// $(window).scroll(positionFooter).resize(positionFooter);
// });
$(document).ready(function(){
function t(){
var e = $("#footer");//获取页脚div的对象
var h = e.offset().top + e.height() ;//获取页脚偏移量加页脚高度的值
//判断页脚div底部到页面顶端的实际距离是否小于页面可见区域高度
if(h < document.body.clientHeight){
//当页面刚好可以包容所有内容不需要下拉时直接加上个定位就是了，当然这里也可以用绝对和相对属性
//具体设置根据你实际情况来定吧
  $("#footer").css({position:"fixed",left:"0",bottom:"0px",marginTop:"20px",borderRadius:"4px"});
  return;
}

function t2(){
  var a = $(document).scrollTop()+document.documentElement.clientHeight;//获取页面滑动偏移量加页面可见区域的高度
//判断页脚div底部到页面顶端的实际距离是否小于页面滑动偏移量加页面可见区域高度
if(a >= h){
//如果页面内容太多，需要下滑展示的时候，给页脚一个固定定位属性
$("#footer").css({position:"fixed",left:"0",bottom:"0px",marginTop:"20px",borderRadius:"4px"});
}else{
//当页面重新上滑页脚需要被隐藏的时候移除它的定位属性，这样不论何时，它肯定是被页面撑起来固定到底部展示的。
 $("#footer").removeAttr("style");
}
}
t2();
//在页面大小改变时触发方法t2
 $(document).resize(t2);
 //在页面滑动时触发方法t2
 $(document).scroll(t2);
}
//直接运行方法t
t();

});