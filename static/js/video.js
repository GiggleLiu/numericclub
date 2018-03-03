var videoMSG
var socket;
var ajinbubbling=false;
var lalabubbling=false;
var timer1;
var timer2;
var lasttime=-1;
var status=-1; //-1 for initial; 1 for ready; 2 for not ready(picking a clip or so)
var bubble_time = 3000;
myname=myname.substr(0,4);
$(document).ready(function(){
    socket = new io.connect("http://"+HOST+":"+PORT);
    socket.on("connect", function() {
        console.log("your are connected to the chat!");
        bubble('ajin',"欢迎来到放映室，发言请按回车。");
        $('#button-ready').text('就绪');
        $('#button-ready').removeClass('btn-warning');
        $('#button-ready').addClass('btn-success');
        send('CON',videoid.toString());
    });
    socket.on("disconnect", function() {
        console.log("your are connected to the chat!");
        bubble('ajin',"连接断开，请检查网络。");
        $('#button-ready').text('未连接');
        $('#button-ready').removeClass('btn-success');
        $('#button-ready').addClass('btn-warning');
    });


    socket.on("MSG", function(message) {
        console.log(message);
        var action=message.substr(0,3);
        var sender=message.substr(3,4);
        var content=message.substr(7);
        handle(action,sender,content);
    });

	video=document.getElementById("myvideo");
    if(ismain){
	    $('#myvideo').on('play',function(){
            send('PLY','');
	    });
	    $('#myvideo').on('pause',function(){
            send('PAU','');
	    });
	    $('#myvideo').on('timeupdate',function(){
		    var ctime=video.currentTime;
		    thistime=parseInt(ctime)
		    if(thistime%10==0 && thistime!=lasttime){
			    lasttime=thistime;
                send('SYN',ctime.toString());
                send('SST',video.paused.toString());
		    }
	    });
	    $('#myvideo').on('seeked',function(){
		    var ctime=video.currentTime;
            send('SYN',ctime.toString());
            send('SST',video.paused.toString());
	    });
    }
	$(window).keyup(windowkeyup);
	$('#input-talk').keyup(talkkeyup);

});

function send(action,message){
    if(isaction(action)){
        socket.emit('MSG',action+myname+message);
    }
    else{
        alert('error action code!');
    }
}
function handle(action,sender,content){
    switch(action){
        case 'MSG':
            bubble(sender,content);
            break;
        case 'PLY':
            if(!ismain){
                video.play();
            }
            break;
        case 'PAU':
            if(!ismain){
                video.pause();
            }
            break;
        case 'SYN':
            if(!ismain){
                time=parseFloat(content);
                if(Math.abs(video.currentTime-time)>1){
                    video.currentTime=time;
                }
            }
            break;
        case 'SST':
            if(!ismain){
                if(content=='true'&&(!video.paused)){video.pause();break;}
                if(content=='false'&&video.paused){video.play();break;}
            }
            break;
        case 'CON':
            if(sender!=myname)
            {
                if(!ismain&&videoid.toString()!=content){
                    bubble('调整您的视频中！');
                    window.location.href="/movie/play/"+content;
                }
                else{
                    if(ismain&&videoid.toString()!=content){
                        send('CON',videoid.toString());
                    }
                    bubble('对方已经连接！');
                }
            }
            break;
        case 'DIS':
            bubble('对方已经失去联络，有事请联系马航机长。');
            break;

        case 'CHN':
            if(!ismain){
                var videosource=document.getElementById('videosource');
                videosource.src=content;
            }
            break;

        default:
            alert(action);
    }
}

function bubble(name,text,color,time,top,left,bgdcolor){
	if(arguments[2]) bubble_color = '#fff';
	if(arguments[3]) bubble_time = 5000;
	if(arguments[4]) bubble_top = 100;
	if(arguments[5]) bubble_left = 100;
	if(arguments[6]) bubble_bgcolor = bgcolor
	var bb=$('#bubble-'+name);
	bb.removeClass('hide');
	$('#bubble-'+name+'-p').text(text);
    if(name=='ajin'){
        if(ajinbubbling){clearTimeout(timer1)};
        ajinbubbling=true;
	    timer1=setTimeout(function(){
			//closeDialog(tagid);
			bb.addClass('hide');
            ajinbubbling=false;
		    },bubble_time+text.length*100);
    }
    if(name=='lala'){
        if(lalabubbling){clearTimeout(timer2)};
        lalabubbling=true;
	    timer2=setTimeout(function(){
			//closeDialog(tagid);
			bb.addClass('hide');
            lalabubbling=false;
		    },bubble_time+text.length*100);
    }
	//divindex=(divindex+1)%5;
}
function newfly(message,y,speed){
	if(!arguments[1]){y=parseInt(Math.random()*(200));}
	if(!arguments[2]){speed=21+parseInt(Math.random()*30);}
	var docwidth=document.body.clientWidth||window.innerWidth;
	var div = document.createElement('div');
	div.className='flydiv';
	//var i=20;
	//var i=docwidth-24*message.length;
	var i=docwidth;
	div.style.left=i+'px';
	div.style.top=y+'px';
	
	div.innerHTML = '<label class="flyfont">'+message+'</label>';
	document.body.appendChild(div);
	
		var timer=setInterval(function(){
		//if(i>docwidth){
		if(i<-20){
    		document.body.removeChild(div); 
			clearInterval(timer);
		}
		else{
			div.style.left=i+'px';
			i=i-3;
			//i=i-1;
		}
	},speed);
}

function fullscreen(){
	$('#myvideo').removeClass('video-normal');
	$('#myvideo').addClass('video-fullscreen');
}
function normalize(vid){
	$('#myvideo').removeClass('video-fullscreen');
	$('#myvideo').addClass('video-normal');
}
function windowkeyup(event) {
	//ESC键
	if(event.keyCode==27){
		if($('#myvideo').hasClass('video-normal')){
			fullscreen();
		}
		else{
			normalize();
		}
	}
	//ENTER键
	else if(event.keyCode==13){
		if($('#div-talk').hasClass('hide')){
			$('#div-talk').removeClass('hide');
			$("#input-talk")[0].focus(); 
		}
		else{
			$('#div-talk').addClass('hide');
		}
	}
}
function talkkeyup(event) {
	//ENTER键
	if(event.keyCode==13){
		if(!$('#div-talk').hasClass('hide')){
			var message=$('#input-talk').val();
			if(message!=''){
				$('#input-talk').val(''); 
				//newfly(message);
				send('MSG',message);
			}
		}
	}
}
function isaction(action){
    if(/^[A-Z]{3}$/i.test(action)) {
        return true
    } else {
        return false
    }
}
