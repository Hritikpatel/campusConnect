const loggedUser = localStorage.getItem("loggedUser");
const isStudent = localStorage.getItem("isStudent");
document.addEventListener("DOMContentLoaded", function() {
	console.log("++++++++++++++++++++++++++");

    const navbarMenu = document.querySelector(".navbar-menu");
    const navbarToggle = document.querySelector(".navbar-toggle");

    navbarToggle.addEventListener("click", function() {
    navbarToggle.classList.toggle("active");
    navbarMenu.classList.toggle("show");
    });


    const teacherOnly = document.querySelector('.isStudent');
    const container = document.querySelector('.studentContainer');
    const tableBody = document.getElementById("table-body");
    const select = document.getElementById('uploadedFor');
    const hiddenVar = document.getElementById("hiddenVar");
    const variable = document.getElementById("variable");

    hiddenVar.value = loggedUser;
    if (loggedUser) {
        $.ajax({
            url: '/informer/',
            data: {'loggedUser': loggedUser, "calledFor": "notes"},
            dataType: 'json',
            success: function(response) {
                var isStudent = response.isStudent;
                var showTo = response.showTo;
                // console.log(isStudent);
                if (isStudent == "N") {
                    teacherOnly.classList.add('teacherOnly');
                    teacherOnly.classList.remove('isStudent')
                    container.classList.add('container');
                    container.classList.remove('studentContainer')
                    for (let i = 0; i < response.fileData.length; i++) {
                        const row = document.createElement("tr");
                        const fileNameCell = document.createElement("td");
                        const uploaderCell = document.createElement("td");
                        const dateCell = document.createElement("td");
                        const emailCell = document.createElement("td");
                        const downloadCell = document.createElement("td");
                        const emailIcon = document.createElement("i");
                        const downloadIcon = document.createElement("a");
                        
                        fileNameCell.textContent = response.fileData[i].fileName;
                        uploaderCell.textContent = response.fileData[i].uploader;
                        dateCell.textContent = response.fileData[i].date;
                        downloadIcon.href = "/static"+response.fileData[i].filePaths;
                        emailIcon.classList.add("fa-solid");
                        emailIcon.classList.add("fa-trash");
                        emailIcon.id = response.fileData[i].pk;
						            emailIcon.classList.add("del");
						            console.log(`add ${emailIcon.classList}`)
                        variable.innerText = "Delete"
                        downloadIcon.classList.add("fa-solid");
                        downloadIcon.classList.add("fa-file-arrow-down");
						

						            emailCell.appendChild(emailIcon);
                        downloadCell.appendChild(downloadIcon);
                        
                        row.appendChild(fileNameCell);
                        row.appendChild(uploaderCell);
                        row.appendChild(dateCell);
                        row.appendChild(downloadCell);
                        row.appendChild(emailCell);
                        
                        tableBody.appendChild(row);
                    }
                      for (let i = 0; i < response.subjectNames.length; i++) {
                          const option = document.createElement('option');
                          option.text = response.subjectNames[i];
                          option.value = response.showTo[i];
                          select.add(option);
                        }
                      setTimeout(addListenersToDelElements, 100);
                      addListenersToDelElements()

                }else{
                  for (let i = 0; i < response.fileData.length; i++) {
                        const row = document.createElement("tr");
                        const fileNameCell = document.createElement("td");
                        const uploaderCell = document.createElement("td");
                        const dateCell = document.createElement("td");
                        const emailCell = document.createElement("td");
                        const downloadCell = document.createElement("td");
                        const emailIcon = document.createElement("i");
                        const downloadIcon = document.createElement("a");
                        
                        fileNameCell.textContent = response.fileData[i].fileName;
                        uploaderCell.textContent = response.fileData[i].uploader;
                        dateCell.textContent = response.fileData[i].date;
                        downloadIcon.href = "/static"+response.fileData[i].filePaths;
                        emailIcon.classList.add('fa-solid');
                        emailIcon.classList.add('fa-envelope');
                        emailIcon.id = response.fileData[i].pk;
                        downloadIcon.classList.add('fa-solid');
                        downloadIcon.classList.add('fa-file-arrow-down');
                        emailCell.appendChild(emailIcon);
                        downloadCell.appendChild(downloadIcon);
                        
                        row.appendChild(fileNameCell);
                        row.appendChild(uploaderCell);
                        row.appendChild(dateCell);
                        row.appendChild(downloadCell);
                        row.appendChild(emailCell);
                        
                        tableBody.appendChild(row);
                      }
                      setTimeout(addListenersToMailElements, 100);
                      addListenersToMailElements()
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
      });
    }else {
        window.location = '/login';
    }
    
	var selectedValues = [];
	var dropdown = document.getElementById("uploadedFor");

	dropdown.addEventListener("change", function() {
		
		dropdown.addEventListener("change", function() {
			
			selectedValues = [];
			
			for (var i = 0; i < dropdown.selectedOptions.length; i++) {
			selectedValues.push(dropdown.selectedOptions[i].value);
		}
	});
	});
});
function add() {
	p = document.getElementById("alert");
  	p.textContent = "Uploading File..."
  
}

function addListenersToDelElements() {
	const del = document.querySelectorAll('.fa-trash');
	console.log(`Found ${del.length} elements with class "del"`);
	del.forEach((element) => {
	  element.addEventListener('click', function() {
		delFile(this.id);
	  });
	});
  
function delFile(id) {
	  console.log(id);
	  $.ajax({
		url: '/informer/',
		data: {'loggedUser': loggedUser, "calledFor": "deleteNotes", "id": id},
		dataType: 'json',
		success: function(response) {
			console.log("done");
			location.reload();
		},
		error: function(xhr, status, error) {
			console.log(xhr.responseText);
		}
	});
	}
}

function addListenersToMailElements() {
    const del = document.querySelectorAll('.fa-envelope');
    console.log(`Found ${del.length} elements with class "Mail"`);
    del.forEach((element) => {
      element.addEventListener('click', function() {
      sendFile(this.id);
      });
    });
    
function sendFile(id) {
      console.log(id);
      $.ajax({
      url: '/informer/',
      data: {'loggedUser': loggedUser, "calledFor": "sendNotes", "id": id},
      dataType: 'json',
      success: function(response) {
        console.log("done");
        location.reload();
      },
      error: function(xhr, status, error) {
        console.log(xhr.responseText);
      }
    });
    }
    }