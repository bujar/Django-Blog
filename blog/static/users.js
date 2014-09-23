var req;

// Sends a new request to update the to-do list
function sendRequest() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "/blog/getUserList", true);
    req.send(); 
}

// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    // Removes the old to-do list users
    var list = document.getElementById("userList");
    if (list != null) {
        while (list.hasChildNodes()) {
            list.removeChild(list.firstChild);
        }
    }
    var list2 = document.getElementById("AnonUserList");
    if (list2 != null) {
        while (list2.hasChildNodes()) {
            list2.removeChild(list2.firstChild);
        }
    }
    // Parses the XML response to get a list of DOM nodes representing users
    var xmlData = req.responseXML;
    var users = xmlData.getElementsByTagName("user");

    // Adds each user to the list
    for (var i = 0; i < users.length; ++i) {
        // Parses the username from the DOM
        var id = users[i].getElementsByTagName("id")[0].textContent
        var username = users[i].getElementsByTagName("text")[0].textContent

        // Builds a new HTML list of users for sidebar
        var newuser = document.createElement("li");
        newuser.innerHTML = "<a href=\"/blog/view_blog/" + username + "\">"+ username + "<img src=\"http://a.dryicons.com/images/icon_sets/coquette_icons_set/png/128x128/add.png\" width=\"20px\" align=\"right\"> </a> ";

        // Adds the todo-list user to the HTML list
        if (list != null) {
        list.appendChild(newuser);
        }


        // Build sidebar list for anonymous user
        var newuser2 = document.createElement("li");
        newuser2.innerHTML = "<a href=\"/blog/view_blog/" + username + "\">"+ username + "</a> ";

        // Adds the todo-list user to the HTML list
        if (list2 != null) {
        list2.appendChild(newuser2);
        }
    }
}

// causes the sendRequest function to run every 10 seconds
window.setInterval(sendRequest, 2000);