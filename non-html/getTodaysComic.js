var today = new Date();
today = today.toLocaleDateString().replace('/', '-').replace('/', '-');

const validFormats = ["jpeg", "jpg", "png", "svg", "webp"];
const comicDisplay = document.getElementById("comic-display");



function urlExists(url) {
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();

    return http.status != 404;
}

var path = ""
var i = 0

validFormats.forEach(function() {
    comicPath = `/dev/comics/${today}.${validFormats[i]}`;

    if (urlExists(`/dev/comics/${today}.${validFormats[i]}`)) { return; }

    i++;
})

// Todays comic wasn't found
if (urlExists(`/dev/comics/${today}.${validFormats[i]}`)) {

} else {
    comicDisplay.setAttribute("src", path);
}