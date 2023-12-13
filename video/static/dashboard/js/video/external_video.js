// var isShow = false;
// function show() {
//   isShow = !isShow;
//   //获取的视频区域。
//   const div = document.querySelector(".add-video-area");
//   //获取的按钮
//   const button = document.querySelector("#open-add-video-btn"); 
  
//   div.style.display = isShow ? "block" : "none";
//   // 添加一个点击了为block的时候，按钮上的文本为编辑中。
// 	//none的时候，按钮上文本为创建。
//   if (isShow) {
// 	  div.style.display = "block";
// 	  button.textContent = "编辑中";
//   } else {
// 	  div.style.display = "none";
// 	  button.textContent = "创建";
//   }
// }
// 第二种方法。是获取id直接使用的。
var videoExternalStatic = false;
//获取区域对象
var videoEditArea = $("#video-edit-area");
$('#open-add-video-btn').click(function() {


  // 添加一个点击了为block的时候，按钮上的文本为编辑中。
	//none的时候，按钮上文本为创建。
	// 显示。
  if (!videoExternalStatic) {
	  videoEditArea.show();
	  // 在id按钮中对象，直接this就可以编辑按钮文本。
	  this.textContent = "编辑中";
	  // alert弹窗。
	  // alert("正在进入编辑--------进入成功。");
  } else {
	  videoEditArea.hide();
	  this.textContent = "创建";
	  // alert("正在关闭编辑--------关闭成功。");
  }
  // 状态取反
	videoExternalStatic = !videoExternalStatic;
});


