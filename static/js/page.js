$(document).ready(function() {	
   startTime();
   initCanvas();
	$('#message').hide();
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
   
   $('.newMsg').bind('tap',function() {     
		  
		  $('#message').css({
		  position: 'fixed',
		  top: 0,
		  left: 0,
		  width: '100%',
		  height: '100%',
		  zIndex: 701,
		  'background-image': 'url(static/img/postit.png)',
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