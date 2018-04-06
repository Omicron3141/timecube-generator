var timer = null;

$(document).ready(function() {
  $("#timeSlider").on("input", onSliderChange);

});

function loadNew(){
  $.get("/new", function(data, status){
    if (status == "success") {
      // send the returned student object to the populate function
      populateNewSentence(data);
    }
  });
}

function populateNewSentence(data){
	$("#quote").html(data);
}

function onSliderChange(){
	var text = "";
	var val = $("#timeSlider").val();
	if (timer != null){
		clearInterval(timer);
	}
	if (val == 0){
		text = "Manual";
	} else {
		text = "Auto: every "+val+"s";
		timer = setInterval(loadNew, val*1000);
	}
	$("#sliderlabel").html(text);

}