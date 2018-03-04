//
//  We wait for the onload function to show that MathJax is laoded after 
//  the page is ready, and then use setTimeout to prove that MathJax is
//  definitely loaded after the page is displayed and active.  MathJax is 
//  loaded two seconds after the page is ready.
//
function showlatex() {
    var head = document.getElementsByTagName("head")[0], script;
    script = document.createElement("script");
    script.type = "text/x-mathjax-config";
    script[(window.opera ? "innerHTML" : "text")] =
      "MathJax.Hub.Config({\n" +
      "  tex2jax: { inlineMath: [['$','$'], ['\\\\(','\\\\)']] }\n" +
      "});"
    head.appendChild(script);
    script = document.createElement("script");
    script.type = "text/javascript";
    script.src  = "/static/js/MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML";
    head.appendChild(script);
}
$(document).ready(function(){
    showlatex();
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

});
function isurl(url){
    if(/^([a-z]([a-z]|\d|\+|-|\.)*):(\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?((\[(|(v[\da-f]{1,}\.(([a-z]|\d|-|\.|_|~)|[!\$&'\(\)\*\+,;=]|:)+))\])|((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=])*)(:\d*)?)(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*|(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)|((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)|((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)){0})(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(url)) {
        return true
    } else {
        return false
    }
}
function isvalidtitle(url){
    if(/^[\w \u4e00-\u9fa5]+$/.test(url)) {
        return true
    } else {
        return false
    }
}
