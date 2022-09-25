$("#add_interview").submit(function (e){
    e.preventDefault();
	var data = new FormData();
	data.append("file", $("input[id^='file']")[0].files[0]);
	data.append("start_time", document.getElementById("start_time").value);
	data.append("end_time", document.getElementById("end_time").value);
	$.ajax({
		method: "POST",
		url: "/schedule/interview/",
		processData: false,
		contentType: false,
		mimeType: "multipart/form-data",
		data: data,
		success: function(response){
			response=JSON.parse(response);
            alert(response.message)
            
		},
        error: function (response){
            alert("Some error occured while enhancing, try again uploading the file.");
        }
	})
    location.reload();
});

$(document)
  .ready(function () {
    $('#table_id')
      .DataTable();
  });

function setIDAndGetInterviewData(id){
	document.getElementById("interview_id").value = id;
	serializedData={"interview_id": id};
	$.ajax({
        type: 'GET',
        url: "get/data/interview/",
        data: serializedData,
        success: function (response) {
            data=JSON.parse(response["data"]);
			student=data[0].fields.student;
			start_time=data[0].fields.start_time;
			end_time=data[0].fields.end_time;
			document.getElementById("for").value=student;
			document.getElementById("st").innerHTML="(Current value is " + start_time + " )";
			document.getElementById("et").innerHTML="(Current value is " + end_time + " )";
        },
        error: function (response) {
            alert(response["responseJSON"]["message"])
        }
    });
}

$("#edit_interview").submit(function (e){
    e.preventDefault();
	var data = new FormData();
	data.append("start_time", document.getElementById("start_time1").value);
	data.append("end_time", document.getElementById("end_time1").value);
	data.append("interview_id", document.getElementById("interview_id").value);
	$.ajax({
		method: "POST",
		url: "/edit/interview/",
		processData: false,
		contentType: false,
		mimeType: "multipart/form-data",
		data: data,
		success: function(response){
			response=JSON.parse(response);
            alert(response.message)
            
		},
        error: function (response){
            alert("Some error occured.");
        }
	})
    location.reload();
});