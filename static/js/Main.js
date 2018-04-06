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