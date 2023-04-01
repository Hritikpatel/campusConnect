document.addEventListener("DOMContentLoaded", function() {
  

	const navbarMenu = document.querySelector(".navbar-menu");
	const navbarToggle = document.querySelector(".navbar-toggle");
	
    navbarToggle.addEventListener("click", function() {
		navbarToggle.classList.toggle("active");
		navbarMenu.classList.toggle("show");
    });
	// Getting today's date
	var date = new Date();
	
	var year = date.getFullYear().toString();
	var month = (date.getMonth() + 1).toString().padStart(2, "0");
	var day = date.getDate().toString().padStart(2, "0");
	
	var today = year + "-" + month + "-" + day;
	
	const startDate = document.getElementById("start-date");
	const endDate = document.getElementById("end-date");
	startDate.value = today;
	endDate.value = today;
	
	// Storing selected options from dropdown
	var selectedValues = [];
	var dropdown = document.getElementById("match-type");
	
	dropdown.addEventListener("change", function() {
		
      dropdown.addEventListener("change", function() {
        
        selectedValues = [];
        
        for (var i = 0; i < dropdown.selectedOptions.length; i++) {
			selectedValues.push(dropdown.selectedOptions[i].value);
        }
		});
	});

	var loggedUser = localStorage.getItem("loggedUser");
	var isStudent = localStorage.getItem("isStudent");

	var inloggedUsers = document.querySelectorAll('input[name="loggedUser"]');
	var inisStudent = document.querySelectorAll('input[name="isStudent"]');
	inloggedUsers.forEach(function(input) {
		input.value = loggedUser;
	});
	inisStudent.forEach(function(input) {
		input.value = isStudent;
	});

	const info = document.getElementById("info");
	var dataToSend = [];

	if (loggedUser) {
		$.ajax({
			url: '/informer/',
			data: {'loggedUser': loggedUser, "calledFor": "timeline", "isStudent": isStudent},
			dataType: 'json',
			success: function(response) {
				if (isStudent == "Y") {
				try {
					info.innerHTML = `<div class="fixedInfo">
					<table>
						<tr>
						<th>Full name</th>
						<td id="fullname"></td>
						</tr>
						<tr>
						<th>Phone</th>
						<td id="phone"></td>
						</tr>
						<tr>
						<th>Email </th>
						<td id="email"></td>
						</tr>
						<tr>
						<th>Set ID </th>
						<td id="setID"></td>
						</tr>
						<tr>
						<th>PRN </th>
						<td id="prn"></td>
						</tr>
						<tr>
						<th>Course </th>
						<td id="course"></td>
						</tr>
						<tr>
						<th>DIV </th>
						<td id="div"></td>
						</tr>
						<tr>
						<th>Semester </th>
						<td id="semester"></td>
						</tr><tr>
						<th>Year </th>
						<td id="year"></td>
						</tr>
						<tr>
						<th>subject </th>
						<td id="subjectNames"></td>
						</tr>
					</table>
					</div>
					<div class="photo"><img src="{% static './media/Default.png' %}" alt="ABS" id="photo"></div>`;
					document.getElementById("fullname").innerText = ":  "+response.fullname;
					document.getElementById("setID").innerText = ":  "+response.setID;
					document.getElementById("prn").innerText = ":  "+response.prn;
					document.getElementById("phone").innerText = ":  "+response.phone;
					document.getElementById("email").innerText = ":  "+loggedUser;
					document.getElementById("course").innerText = ":  "+response.course;
					document.getElementById("div").innerText = ":  "+response.Div;
					document.getElementById("semester").innerText = ":  "+response.sem;
					document.getElementById("year").innerText = ":  "+response.year;

					document.getElementById("subjectNames").innerText = ":  "+response.subjectNames;
					$('.photo img').attr('src', "/static"+response.image);
				} catch (error) {
					console.log("You are looking at Timetable result");
				}
				} else {
				try {
						info.classList.add("faculty");
						info.classList.remove("resultContainer");
						const subName = document.getElementById("subName");
						$('#subName').empty();
						response.subjectNames.forEach(element => {
							const opt = document.createElement("option");
							opt.value = element;
							opt.textContent = element;
							subName.appendChild(opt);
					});
				} catch (error) {
					console.log("You are looking at Timetable result");
				}
				}
					
				$.ajax({
				url: '/informer/',
				data: {'loggedUser': loggedUser, "calledFor": "lecture", "isStudent": isStudent},
				dataType: 'json',
				success: function(response) {
					$('.timeLine').empty();
					$('<p>').html(" Today's Lectures").appendTo($('.timeLine'));
					for (var lecture in response.lectures) {
					var details = $('<details>').appendTo($('.timeLine'));
					var summary = $('<summary>').addClass('summaryTitle').appendTo(details);
					$('<div>').addClass("flex-items").attr("id", "startTime").html(response.lectures[lecture]['startTime']).appendTo(summary);
					$('<div>').addClass("flex-items").attr("id", "subjectName").html(response.lectures[lecture]['subjectName']).appendTo(summary);
					$('<div>').addClass("flex-items").attr("id", "roomNo").html(response.lectures[lecture]['roomNo']).appendTo(summary);
					var content = $('<div>').addClass('content').appendTo(details);
					$('<div>').html(' Subject: ' + response.lectures[lecture]['subjectName']).appendTo(content);
					$('<div>').html(' Room No: ' + response.lectures[lecture]['roomNo']).appendTo(content);
					$('<div>').html(' Time: ' + response.lectures[lecture]['startTime']+" - "+response.lectures[lecture]['endTime']).appendTo(content);
					}
					$('.inTimeline').empty();
					$('<p>').html(" Today's TODO ").appendTo($('.inTimeline'));
					for (var lecture in response.todo) {
					var details = $('<details>').appendTo($('.inTimeline'));
					var summary = $('<summary>').addClass('summaryTitle').appendTo(details);
					$('<div>').addClass("flex-items").attr("id", "startTime").html("").appendTo(summary);
					$('<div>').addClass("flex-items").attr("id", "subjectName").html(response.todo[lecture]['title']).appendTo(summary);
					$('<div>').addClass("flex-items").attr("id", "roomNo").html("").appendTo(summary);
					var content = $('<div>').addClass('content').html(' Title: ' + response.todo[lecture]['title']).appendTo(details);
					$('<div>').html(' Desc: ' + response.todo[lecture]['desc']).appendTo(content);
					$('<div>').html(' Time: ' + response.todo[lecture]['time']).appendTo(content);
					}

					class Accordion {
					constructor(el) {
						// Store the <details> element
						this.el = el;
						// Store the <summary> element
						this.summary = el.querySelector('summary');
						// Store the <div class="content"> element
						this.content = el.querySelector('.content');
						this.startTime = el.querySelector("#startTime");
						this.startTitle = this.startTime.textContent;
						this.subjectName = el.querySelector("#subjectName");
						this.subjectTitle = this.subjectName.textContent;
						this.roomNo = el.querySelector("#roomNo");
						this.roomTitle = this.roomNo.textContent;
						// Store the animation object (so we can cancel it if needed)
						this.animation = null;
						// Store if the element is closing
						this.isClosing = false;
						// Store if the element is expanding
						this.isExpanding = false;
						this.isClosed = true
						// Detect user clicks on the summary element
						this.summary.addEventListener('click', (e) => this.onClick(e));
					}

					onClick(e) {
						// Stop default behaviour from the browser
						e.preventDefault();
						// Add an overflow on the <details> to avoid content overflowing
						this.el.style.overflow = 'hidden';
						// Check if the element is being closed or is already closed
						if (this.isClosing || !this.el.open) {
						this.open();
						// Check if the element is being openned or is already open
						} else if (this.isExpanding || this.el.open) {
						this.shrink();
						}
						this.change();
					}
					change(e){
						if (!this.isClosed) {
						this.startTime.textContent = this.startTitle;
						this.subjectName.textContent = this.subjectTitle;
						this.roomNo.textContent = this.roomTitle;
						this.isClosed = true;
						}else{
						this.startTime.textContent = "";
						this.subjectName.textContent = "Lecture Information";
						this.roomNo.textContent = "";
						this.isClosed = false
						}
					}
					
					shrink() {
						// Set the element as "being closed"
						this.isClosing = true;
						
						// Store the current height of the element
						const startHeight = `${this.el.offsetHeight}px`;
						// Calculate the height of the summary
						const endHeight = `${this.summary.offsetHeight}px`;
						
						// If there is already an animation running
						if (this.animation) {
						// Cancel the current animation
						this.animation.cancel();
						}
						
						// Start a WAAPI animation
						this.animation = this.el.animate({
						// Set the keyframes from the startHeight to endHeight
						height: [startHeight, endHeight]
						}, {
						duration: 400,
						easing: 'ease-out'
						});
						
						// When the animation is complete, call onAnimationFinish()
						this.animation.onfinish = () => this.onAnimationFinish(false);
						// If the animation is cancelled, isClosing variable is set to false
						this.animation.oncancel = () => this.isClosing = false;
					}
					
					open() {
						// Apply a fixed height on the element
						this.el.style.height = `${this.el.offsetHeight}px`;
						// Force the [open] attribute on the details element
						this.el.open = true;
						// Wait for the next frame to call the expand function
						window.requestAnimationFrame(() => this.expand());
					}
					
					expand() {
						// Set the element as "being expanding"
						this.isExpanding = true;
						// Get the current fixed height of the element
						const startHeight = `${this.el.offsetHeight}px`;
						// Calculate the open height of the element (summary height + content height)
						const endHeight = `${this.summary.offsetHeight + this.content.offsetHeight}px`;
						
						// If there is already an animation running
						if (this.animation) {
						// Cancel the current animation
						this.animation.cancel();
						}
						
						// Start a WAAPI animation
						this.animation = this.el.animate({
						// Set the keyframes from the startHeight to endHeight
						height: [startHeight, endHeight]
						}, {
						duration: 400,
						easing: 'ease-out'
						});
						// When the animation is complete, call onAnimationFinish()
						this.animation.onfinish = () => this.onAnimationFinish(true);
						// If the animation is cancelled, isExpanding variable is set to false
						this.animation.oncancel = () => this.isExpanding = false;
					}
					
					onAnimationFinish(open) {
						// Set the open attribute based on the parameter
						this.el.open = open;
						// Clear the stored animation
						this.animation = null;
						// Reset isClosing & isExpanding
						this.isClosing = false;
						this.isExpanding = false;
						// Remove the overflow hidden and the fixed height
						this.el.style.height = this.el.style.overflow = '';
					}
					}
					
					document.querySelectorAll('details').forEach((el) => {
					new Accordion(el);
					});  
				},
				error: function(xhr, status, error) {
					console.log(xhr.responseText);
				}
			});
			},
			error: function(xhr, status, error) {
				console.log(xhr.responseText);
			}
		});
	}else {
		window.location = '/login';
	}
	
	
	try {
		const planChange = document.getElementById("check");
		planChange.addEventListener("click", function(){
			var date = document.getElementById("date").value;
			var subject = document.getElementById("subName").value;
			var plan = document.getElementById("planChange").value;

			if (plan == "cancel") {
				
				$.ajax({
					url: '/informer/',
					data: {'loggedUser': loggedUser, "calledFor": "getLecture", "isStudent": isStudent, "date" : date, "subject": subject},
					dataType: 'json',
					success: function(response) {
	
						const table = document.getElementById("possibleTable");
						const p = document.getElementById("msg");
						$('#possibleTable').empty();
						if (response.data.length == 1) {
							p.textContent = "No Lecture on given date";	
						} else {
							
							for (var i = 0; i < response.data.length; i++) {
							var row = table.insertRow(i);
							
							for (var j = 0; j < response.data[i].length; j++) {
								var cell = row.insertCell(j);
								cell.innerHTML = response.data[i][j];
							}
							}
							p.textContent = "Click on lecture you want to cancel.";
							const rows = table.querySelectorAll('tr');
							rows.forEach(row => { 
							row.addEventListener('click', () => { 
								var data = row.querySelectorAll("td");
								data.forEach(text => {
									// console.log(text.innerText);
									dataToSend.push(text.innerText);
								});
								dataToSend.push(subject);
								$.ajax({
									url: '/informer/',
									data: {'loggedUser': loggedUser, "calledFor": "lectureCancelled", "isStudent": isStudent, "data" : JSON.stringify(dataToSend)},
									dataType: 'json',
									success: function(response) {
										p.textContent = response.data;
									},
									
									error: function(xhr, status, error) {
										console.log(xhr.responseText);
									}
								});
							});
						});
						
						}
	
					},
					
					error: function(xhr, status, error) {
						console.log(xhr.responseText);
					}
				});
			} else {
				console.log("add");
			}
		});
	} catch (error) {
		console.log(error);
	}
});