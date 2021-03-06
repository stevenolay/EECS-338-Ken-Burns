

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

function makePremade(name){
	var param = name;
	console.log("Called premade")
	var child = document.getElementById("jumbotron");
	if(child != null){
		child.parentNode.removeChild(child);
		console.log("removed jumbotron");
		document.getElementById('progress').style.display = "block";
		document.getElementById('images').style.display = "block";
	}
	else{
		console.log("no jumbotron");
		var child = document.getElementById('rectangle');
		child.parentNode.removeChild(child);
	}

	var videoSrc = makeCall(param);

}

function make2(){
	var child = document.getElementById("progress");
    child.parentNode.removeChild(child);
    var child = document.getElementById("images");
    child.parentNode.removeChild(child);
	document.getElementById('rectangle').style.display = "block";
}

function showAbout(){
	document.getElementById('aboutcard').scrollIntoView(false);
	console.log("In about card function.")
}

function showHowTo(){
	document.getElementById('howto').scrollIntoView(false);
	console.log("In about card function.")
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
						video.width = 1200;
						video.id = 'video-box';
						var par = document.getElementById('parent');
						par.height = 675;
						par.appendChild(video);
						var curr = document.getElementById("progress");
						curr.parentElement.removeChild(curr);
						var curr = document.getElementById("images");
						curr.parentElement.removeChild(curr);
            return data;
        }
    });
}
