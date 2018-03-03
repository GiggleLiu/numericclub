var imagelist=new Array();
function isimageurl(url){
    var b=isurl(url);
    tag=url.split('.').pop();
    if(b&&(tag=='jpg'||tag=='gif'||tag=='png')){
        return true
    }
    else{return false}
}
function isdate(date) {
    return (/^\d{4}-\d?\d-\d?\d$/).test(date);
}
function addimage(target,url){
if(isimageurl(url)){
        l=String(imagelist.length);
        $(target).prepend('<div class="col-xs-6 col-md-3" id="div-img-'+l+'"><a href="#" class="thumbnail"><img src="'+url+'" alt="" onerror="alert(\'error!\')"><a href="#" id="'+l+'" onclick="removeimage('+l+')">删除</a></div>');
        imagelist.push(url);
    }
    else{alert('Not a valid image url. Accept only jpg/png/gif')}
}
function removeimage(index){
    $('#div-img-'+index).remove();
    delete imagelist[parseInt(index)];
}

