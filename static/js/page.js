var messageBlinkId;

$(document).ready(function() {	
   startTime();
   //initCanvas();
   canvas   = document.getElementById('can');
   signaturePad = new SignaturePad(canvas);
   $('#message').hide();
   $('#messageNew').hide();
   
   initMessageShowTap();
   
   //close new message
   $('#messageShowClose').bind('tap',function() {
       $('#messageShow').hide();
       window.clearInterval(messageBlinkId);    
       $('#imgMessageNew').remove();  
   });   
   
   
   $('.station').bind('tap',function() {  
	
		var src=$(this).attr('src');
		
		var myRegexp = /.+\/btn-(.+)\.png$/g;
		var match = myRegexp.exec(src);
		var station = match[1];
		
		var area=$(this).parent().parent().text().trim();
		
		var ip;
		if (area==='BATHROOM'){
			ip="192.168.178.31"
		}
		else if (area==='LIVINGROOM'){
			ip="192.168.178.37"
		}
		else {
			return;
		}
		
		$.ajax('http://localhost:5000/tune?target='+ip+'&station='+station);
		
   });
   
   
   
   $('#trash').bind('tap',function() {  
	
        canvas = document.getElementById('can');
        ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
		$('#message').hide();
		
   });
   
   //canvas save
   $('#save').bind('tap',function() {  
	
        canvas = document.getElementById('can');
		var dataUrl = canvas.toDataURL();
        var filename = Date.now() + '.png';
        dataUrl = dataUrl.replace('data:image/png;base64,','');
        ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        $.post( "http://localhost:5000/save", { dataUrl: dataUrl, filename: filename} );
		$('#message').hide();
        $('#messageNew').html('<img id="imgMessageNew" style="cursor:pointer;" height="128" width="128" src="static/img/message.png" />');
        initMessageShowTap();
        $('#messageNew').show();
        messageBlinkId = setInterval(messageBlink, 1500);
        
        
   });
   
   
   
   $('.newMsg').bind('tap',function() {     
		  
		  $('#message').css({
		  position: 'fixed',
		  top: 0,
		  left: 0,
		  width: '100%',
		  height: '100%',
		  zIndex: 701,
		  'background-image': 'url(static/img/paper.png)',
		  'background-repeat':'no-repeat'

		});
		$('#message').show();
   });
   
   $('.boxheader').bind('tap',function() {  
	
		var area=$(this).text().trim();
		
		var ip;
		if (area==='BATHROOM'){
			ip="192.168.178.31"
		}
		else if (area==='LIVINGROOM'){
			ip="192.168.178.37"
		}
		else {
			return;
		}
		
		$.ajax('http://localhost:5000/stop?target='+ip);
		
   });
});

function initMessageShowTap(){
    //show new message
   $('#imgMessageNew').bind('tap',function() {       
       $('#messageNew').hide();       
       $('#messageShow').show();
       $('#messageShowContent').html($('<img />').attr('src','/getMessages'));
       
       
   });  
}

function messageBlink() {
    $('#messageNew').fadeOut(1500).fadeIn(1500);    
}

function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('time').innerHTML = h + ":" + m;
    var t = setTimeout(startTime, 15000);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}