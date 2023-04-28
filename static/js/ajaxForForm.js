const loginField = document.getElementById('myemailid');
loginField.addEventListener("change", function () {
    let myemailid = 'myemailid=' + this.value;
    // var url = loginField.dataset.url;
    let csrftoken = getCookie();
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'ajax/form/', true);
    xhr.addEventListener('readystatechange', function () {
        if ((xhr.readyState == 4) && (xhr.status == 200)) {
            let data = JSON.parse(xhr.response);

            const response = document.querySelector('.ajax-field-valid');
            response.innerHTML = data.message;
            if (data.otkl == 1) {
                document.getElementById("sybmitbtn").disabled = true;
            } else {
                document.getElementById("sybmitbtn").disabled = false;
            }
        }
    });
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(myemailid);
});

const emailField = document.getElementById('myloginid');
emailField.addEventListener("change", function () {
    let myloginid = 'myloginid=' + this.value;
    // var url = loginField.dataset.url;
    let logincsrftoken = getCookie();
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'ajax/formlogin/', true);
    xhr.addEventListener('readystatechange', function () {
        if ((xhr.readyState == 4) && (xhr.status == 200)) {
            let data = JSON.parse(xhr.response);

            const response = document.querySelector('.ajax-field-valid');
            response.innerHTML = data.message;
            if (data.otkl == 1) {
                document.getElementById("sybmitbtn").disabled = true;
            } else {
                document.getElementById("sybmitbtn").disabled = false;
            }
        }
    });
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", logincsrftoken);
    xhr.send(myloginid);
});

const passField = document.getElementById('mypassid');
passField.addEventListener("change", function () {
    let mypassid = 'mypassid=' + this.value;
    // var url = loginField.dataset.url;
    let passcsrftoken = getCookie();
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'ajax/formpass/', true);
    xhr.addEventListener('readystatechange', function () {
        if ((xhr.readyState == 4) && (xhr.status == 200)) {
            let data = JSON.parse(xhr.response);

            const response = document.querySelector('.ajax-field-valid');
            response.innerHTML = data.message;
            if (data.otkl == 1) {
                document.getElementById("sybmitbtn").disabled = true;
            } else {
                document.getElementById("sybmitbtn").disabled = false;
            }
        }
    });
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", passcsrftoken);
    xhr.send(mypassid);
});

const pass2Field = document.getElementById('mypass2id');
pass2Field.addEventListener("change", function () {
    let mypass2id = 'mypass2id=' + this.value;
    // var url = loginField.dataset.url;
    let pass2csrftoken = getCookie();
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'ajax/formpass2/', true);
    xhr.addEventListener('readystatechange', function () {
        if ((xhr.readyState == 4) && (xhr.status == 200)) {
            let data = JSON.parse(xhr.response);

            const response = document.querySelector('.ajax-field-valid');
            response.innerHTML = data.message;
            if (data.otkl == 1) {
                document.getElementById("sybmitbtn").disabled = true;
            } else {
                document.getElementById("sybmitbtn").disabled = false;
            }
        }
    });
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", pass2csrftoken);
    xhr.send(mypass2id);
});

function getCookie() {
    //let cook = document.cookie.split('=');
    var cook = $('input[name="csrfmiddlewaretoken"]').val();
    return cook;
}