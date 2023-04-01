window.onload = function() {

    const navbarMenu = document.querySelector(".navbar-menu");
    const navbarToggle = document.querySelector(".navbar-toggle");

    navbarToggle.addEventListener("click", function() {
    navbarToggle.classList.toggle("active");
    navbarMenu.classList.toggle("show");
    });


    
    const loggedUser = localStorage.getItem("loggedUser");
    const isStudent = localStorage.getItem("isStudent");
    const container = document.querySelector('.studentContainer');
    const teacherOnly = document.querySelector('.isStudent');

    const sheetForm = document.getElementById("sheetForm");
    var subjectTypes = [];
    var subjectName = [];
    const form = document.createElement('form');
    const workBookLabel = document.createElement('label');
    const saveButton = document.createElement('button');
    const urlLabel = document.createElement('label');
    const verifySpan = document.createElement('span');
    const rotateIcon = document.createElement('i');
    const urlInput = document.createElement('input');
    const select = document.createElement('select');
    const subjectLabel = document.createElement("label");
    const divSelect = document.createElement('select');
    divSelect.id = "divSelect"
    divSelect.innerHTML = `
                            <option value="A">A</option>
                            <option value="B">B</option>
                            <option value="C">C</option>
                            <option value="D">D</option>
                            <option value="E">E</option>
                            `;
    const dataTab = document.getElementById("dataTab");
    const dataGoesHere = document.getElementById("dataGoesHere");
    const childElement = dataTab.querySelector('.loading');

    if (isStudent == "N") {
        teacherOnly.classList.add('sheetForm');
        teacherOnly.classList.remove('isStudent')
        container.classList.add('container');
        container.classList.remove('studentContainer')
    }
    if (loggedUser) {
        $.ajax({
            url: '/informer/',
            data: {'loggedUser': loggedUser, "calledFor": "attendance", "isStudent": isStudent},
            dataType: 'json',
            success: function(response) {
                if (isStudent == "N") {
                    
                    urlLabel.htmlFor = 'url';
                    urlLabel.appendChild(document.createTextNode('Workbook shared Link'));
                    verifySpan.id = 'verify';
                    rotateIcon.className = 'fa-solid fa-rotate-right';
                    verifySpan.appendChild(rotateIcon);
                    urlInput.type = 'url';
                    urlInput.name = 'url';
                    urlInput.id = 'url';
                    urlInput.placeholder = "Paste Workbook Link"
                    workBookLabel.htmlFor = 'sheetName';
                    workBookLabel.appendChild(document.createTextNode('Sheet Name'));
                    saveButton.type = 'button';
                    saveButton.className = 'submitBtn';
                    saveButton.id = 'submitBtn';
                    saveButton.name = 'submitBtn';
                    saveButton.disabled;
                    saveButton.appendChild(document.createTextNode('Save'));


                    console.log(response.subjectNames);
                    subjectName = response.subjectNames;
                    subjectTypes = response.subjectTypes;
                    subjectLabel.htmlFor = 'Subject';
                    subjectLabel.appendChild(document.createTextNode('Subject'));
                    select.id = "subjects";
                    select.name = "subjects";
                    subjectName.forEach(name => {
                        const opt = document.createElement('option');
                            opt.value = name;
                            opt.appendChild(document.createTextNode(name));
                            select.appendChild(opt);
                        
                        });

                    form.appendChild(subjectLabel);
                    form.appendChild(select);
                    var selected = select.value;
                    for (let i = 0; i < subjectTypes.length; i++) {
                        if (subjectTypes[i] == "Base") {
                            if (subjectName[i] == selected) {
                                
                                form.appendChild(divSelect);
                        }
                    }  
                    form.appendChild(urlLabel);
                    form.appendChild(verifySpan);
                    form.appendChild(urlInput);
                    sheetForm.appendChild(form);
                    try {
                        dataTab.removeChild(childElement);
                    } catch (error) {
                        console.log(error);
                    }

                    

                }
                
                
                }else{
                    
                    var data = response.data;
                    var percentage = 0;
                    for (const key in data) {
                        const table = document.createElement("table");
                        table.border = "2px";
                        const tbody = document.createElement("tbody");
                        var h4 = document.createElement("h4");
                        if (data.hasOwnProperty.call(data, key)) {
                            const element = data[key];
                            h4.innerText = key;
                            // console.log(element)
                            
                            for (const x in element) {
                                const tr = document.createElement("tr");
                                const th = document.createElement("th");
                                if (x == "Attendance") {
                                    const total = element[x].length;
                                    const present = element[x].filter(a => a === 'P').length;
                                    percentage = (present / total) * 100;
                                }
                                th.innerText = x;
                                tr.appendChild(th);
                                if (element.hasOwnProperty.call(element, x)) {
                                    element[x].forEach(info => {
                                        const td = document.createElement("td");
                                        td.innerText = info
                                        tr.appendChild(td)
                                    });
                                }
                                tbody.appendChild(tr)
                            }
                        table.appendChild(tbody)
                    }
                    h4.innerText =  h4.innerText+"   |   "+percentage.toFixed(2)+"%";
                    
                    dataGoesHere.appendChild(h4);
                    dataGoesHere.appendChild(table)
                }
                try {
                    dataTab.removeChild(childElement);
                } catch (error) {
                    console.log(error);
                }
                
                }

            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
    }else {
        window.location = '/login';
    }
    
    
    const help = document.getElementById("help");
    help.addEventListener("click", showHelp);
    function showHelp() {
        alert("Copy text >> open attendance sheet >> open share section >> paste text in 'Add people or groups' section >> change permission to viewer >> come back and hit save.\n or \n Go to 'General access' section and copy link and paste url in url section.")
    }
    
    const code = document.getElementById("code-section");
    code.addEventListener("click", copyCode);
    function copyCode() {
        var id = code.innerText;
        navigator.clipboard.writeText(id);
        
        // Update button text after copying
        code.innerHTML = id+'<i style="color: green;" class="fas fa-check"></i>';
        setTimeout(function() {
            code.innerHTML = id+'<i class="fas fa-copy"></i>';
        }, 1500); // Reset button text after 1 second
    }
    
    verifySpan.addEventListener("click", verifyFunction);
    function verifyFunction() {
        verifySpan.innerHTML = '<i class="fa-solid fa-rotate-right fa-spin" id="verify"></i>'
        var url = document.getElementById("url").value;
        $.ajax({
            url: '/informer/',
            data: {'loggedUser': loggedUser, "calledFor": "verify", "isStudent": isStudent, "url": url},
            dataType: 'json',
            success: function(response) {
                console.log("Single");
                const form = document.querySelector('form');
                const sheetLabel = document.createElement("label");
                sheetLabel.htmlFor = 'Sheet';
                sheetLabel.appendChild(document.createTextNode('Sheet'));
                sheetLabel.id = "sheetLabel";
                sheetLabel.name = "sheet";
                
                const select = document.createElement('select');
                select.id = "sheet";
                select.name = "sheet";
                // Array of sheet names
                const sheetNames = response.sheet_names;
                sheetNames.forEach(name => {
                    const opt = document.createElement('option');
                      opt.value = name;
                      opt.appendChild(document.createTextNode(name));
                      select.appendChild(opt);
                  
                    });
                form.appendChild(sheetLabel);
                form.appendChild(select);
                form.appendChild(saveButton);
                verifySpan.innerHTML = '<i style="color: green;" class="fa-solid fa-check"></i>';
                if (response.status == "OK") {
                } else if(response.status == "Multi"){
                    console.log("Multi");
                }else {
                    verify.innerHTML = '<i style="color: red;" class="fa-solid fa-xmark"></i>';
                }
                var sheet = document.getElementById("sheet");
                    sheet.addEventListener("change", function () {
                        $.ajax({
                            url: '/informer/',
                            data: {'loggedUser': loggedUser, "calledFor": "getSheet", "isStudent": isStudent},
                            dataType: 'json',
                            success: function(response) {
                                console.log(response);
                            },
                            error: function(xhr, status, error) {
                                console.log(xhr.responseText);
                            }
                        });
                        

                    });
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });

    }

    select.addEventListener("change", checkDiv);
    function checkDiv() {
        try {
            form.removeChild(divSelect)
        } catch (error) {
            console.error();
        }
        var selected = select.value;
        for (let i = 0; i < subjectTypes.length; i++) {
           if (subjectTypes[i] == "Base") {
                if (subjectName[i] == selected) {
                    divSelect.innerHTML = `
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="E">E</option>
                    `;
                    form.appendChild(divSelect);
                }
            }
        }
        form.appendChild(urlLabel);
        form.removeChild(verifySpan);
        form.removeChild(urlInput);
        sheetForm.removeChild(form);

        
        form.appendChild(urlLabel);
        form.appendChild(verifySpan);
        form.appendChild(urlInput);
            
            
        sheetForm.appendChild(form);
    }
    


    const submitBtn = saveButton;
    submitBtn.addEventListener("click", store);
    function store() {
        var subject = document.getElementById("subjects").value;
        var urlShared = document.getElementById("url").value;
        var sheet = document.getElementById("sheet").value;
        var selectedDiv = "";
        try {
            selectedDiv = document.getElementById("divSelect").value;
        } catch (error) {
            console.error(error);
        }

        console.log(selectedDiv);
        $.ajax({
            url: '/informer/',
            data: {'loggedUser': loggedUser, "calledFor": "saveAttendance", "subject": subject, "urlShared": urlShared, "sheet": sheet, "Div": selectedDiv},
            dataType: 'json',
            success: function(response) {
                document.getElementById("msg").innerText = "Data saved... reloading..."
                window.location = "/attendance"
                  console.log("Done");
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });

    }
}