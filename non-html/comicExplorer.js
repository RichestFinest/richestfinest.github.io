// Show the latest comic

const validFormats = ["jpeg", "jpg", "png", "svg", "webp"];
var comicDisplay = document.getElementById("comic-display");

var today = new Date();
today = today.toLocaleDateString().replace('/', '-').replace('/', '-');

var todaysComic = null;

function urlExists(url) {
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();

    return http.status != 404;
}

var comicExists = false;
var daysSinceLastComic = 0
var possibleComic = null;

while (!comicExists) {
    day = new Date(today)
    day.setDate(day.getDate() - daysSinceLastComic)
    day = day.toLocaleDateString().replace('/', '-').replace('/', '-');


    var forLoop = true;
    validFormats.forEach(function(format) {
        if (!forLoop) { return; }
        possibleComic = `/dev/comics/${day}.${format}`;

        if (urlExists(possibleComic)) {
            comicExists = true;
            forLoop = false;

            return;
        }
    })

    daysSinceLastComic++;
}

comicDisplay.setAttribute("src", possibleComic)

// Button functionality
var firstComicDate = new Date(2022, 7, 21, 0, 0, 0, 0) // the monthIndex is 7 when it should be 8, but js is being weird

document.getElementById("previous-comic-button").addEventListener("click", function() {
    comicExists = false;
    while (!comicExists) {
        var rawDay = new Date(today)
        rawDay.setDate(rawDay.getDate() - daysSinceLastComic)
        day = rawDay.toLocaleDateString().replace('/', '-').replace('/', '-');

        if (rawDay < firstComicDate) {
            window.alert("You've reached the first comic. No going further!")
            break;
        }
    
    
        var forLoop = true;
        validFormats.forEach(function(format) {
            if (!forLoop) { return; }
            possibleComic = `/dev/comics/${day}.${format}`;
    
            if (urlExists(possibleComic)) {
                comicExists = true;
                forLoop = false;
    
                return;
            }
        })
    
        daysSinceLastComic++;
    }

    comicDisplay.setAttribute("src", possibleComic)
})

document.getElementById("next-comic-button").addEventListener("click", function() {
    comicExists = false;
    while (!comicExists) {
        var rawDay = new Date(today)
        rawDay.setDate(rawDay.getDate() - daysSinceLastComic + 2)
        day = rawDay.toLocaleDateString().replace('/', '-').replace('/', '-');

        if (rawDay < firstComicDate) {
            window.alert("You've reached the first comic. No going further!")
            break;
        }

        if (rawDay > new Date()) {
            window.alert("This is the most recent comic. No going further!")
            break;
        }
    
        var forLoop = true;
        validFormats.forEach(function(format) {
            if (!forLoop) { return; }
            possibleComic = `/dev/comics/${day}.${format}`;
    
            if (urlExists(possibleComic)) {
                comicExists = true;
                forLoop = false;
    
                return;
            }
        })
    
        daysSinceLastComic--;
    }

    comicDisplay.setAttribute("src", possibleComic)
})
