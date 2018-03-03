$(document).ready(function(){
	$(".trigger").click(function() {
	   	if($("#"+this.id+'-content').hasClass("hide")){
	   		$("#"+this.id+'-content').removeClass("hide");
	   	}
	   	else{
	   		$("#"+this.id+'-content').addClass("hide");
	   	}
	});
	$(".hover").on('mouseenter click',function() {
		   	if($("#"+this.id+'-content').hasClass("hide")){
		   		$("#"+this.id+'-content').removeClass("hide");
		   	}
	   	});
    $('.hover').on('mouseleave',function(){
		   	if(!$("#"+this.id+'-content').hasClass("hide")){
		   		$("#"+this.id+'-content').addClass("hide");
	    	}
    });
	$('.modal-form').on('submit', function(){

		// Hide the modal
		$(".modal").modal('hide');
	
	});

    //init the datetimepicker of law page
    //$('#end-date').datetimepicker({
        //language:  'zh-CN',
        //format: 'yyyy年mm月dd日',
        //weekStart: 1,
        //todayBtn:  1,
        //autoclose: 1,
        //todayHighlight: 1,
        //startView: 2,
        //forceParse: 0,
        //showMeridian: 1
    //});
 
});
function isurl(url){
    if(/^([a-z]([a-z]|\d|\+|-|\.)*):(\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?((\[(|(v[\da-f]{1,}\.(([a-z]|\d|-|\.|_|~)|[!\$&'\(\)\*\+,;=]|:)+))\])|((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=])*)(:\d*)?)(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*|(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)|((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)|((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)){0})(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(url)) {
        return true
    } else {
        return false
    }
}
//single previewer
function readURL(targetid,input,i) {
    if(!arguments[2]) i=0;
    if (input.files && input.files[i]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#'+targetid).attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[i]);
    }
}
//multiple previewer
function mreadURL(targetid,input) {
    var len=input.files.length;
    var html='';
    for(var i=0;i<len;i++){
        var reader = new FileReader();
        reader.onload = function (e) {
            html+='<div class="col-md-3"><div class="thumbnail"><img src="'+e.target.result+'"></div></div>';
            //$('#'+targetid).attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[i]);
    }
    setTimeout(function(){
        $('#'+targetid).html(html);
    },200);
}
