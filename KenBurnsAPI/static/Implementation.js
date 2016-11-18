

function inputFocus(i){
	if(i.value==i.defaultValue){ i.value=""; i.style.color="#000"; }
}

function inputBlur(i){
    if(i.value==""){ i.value=i.defaultValue; i.style.color="#888"; }
}

function make(){

	var param = document.getElementById("input").value;


	var child = document.getElementById("jumbotron");
    child.parentNode.removeChild(child);
	document.getElementById('progress').style.display = "block";
	document.getElementById('images').style.display = "block";

	var videoSrc = makeCall(param);


}

function make2(){
	var child = document.getElementById("progress");
    child.parentNode.removeChild(child);
    var child = document.getElementById("images");
    child.parentNode.removeChild(child);
	document.getElementById('rectangle').style.display = "block";
}

function makeCall(input){
	var url = "http://localhost:5000/fetch/" + input;
	$.ajax({
        url: url,
        type: 'GET',
        //dataType: 'json', // added data type
        success: function(res) {
            var data = res;
            console.log(data);

						videoSrc = "/static/output_videos/" + data;
						var video = document.createElement('video');
						video.autoplay = true;
						video.setAttribute("controls", "controls");
						video.src =  videoSrc;
						video.width = 700;
						video.id = 'video-box';
						document.getElementById('parent').appendChild(video);
						var curr = document.getElementById("progress");
						curr.parentElement.removeChild(curr);
						var curr = document.getElementById("images");
						curr.parentElement.removeChild(curr);
            return data;
        }
    });
}
