var today = new Date();
today = today.toLocaleDateString().replace('/', '-').replace('/', '-');

var yesterday = new Date(today)
yesterday.setDate(yesterday.getDate() - 1)

yesterday = yesterday.toLocaleDateString().replace('/', '-').replace('/', '-');

const validFormats = ["jpeg", "jpg", "png", "svg", "webp"];
const comicDisplay = document.getElementById("comic-display");
const comicStatus = document.getElementById("comic-status");



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


if (urlExists(`/dev/comics/${today}.${validFormats[i]}`)) {
    comicDisplay.setAttribute("src", comicPath);
} else {
    i = 0;
    // Todays comic wasn't found
    validFormats.forEach(function() {
        comicPath = `/dev/comics/${yesterday}.${validFormats[i]}`;
    
        if (urlExists(`/dev/comics/${yesterday}.${validFormats[i]}`)) { return; };
    
        i++;
    })

    if (urlExists(`/dev/comics/${yesterday}.${validFormats[i]}`)) {
        // Yesterday's comic was found
        comicStatus.textContent = "Today's comic has not been published yet. Here's yesterday's comic.";
        comicDisplay.setAttribute("src", comicPath);
    } else {
        comicStatus.style.color = "red"
        comicStatus.innerHTML = "No comic was uploaded today or yesterday. <br>You can check the <a href=https://discord.gg/KUW5WsagkM target=_blank>Discord server</a> for more information, or check the <a href=/gallery.html>Gallery</a>."
    }
}