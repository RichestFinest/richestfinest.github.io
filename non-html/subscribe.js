// Import the functions you need from the SDKs you need
import { getFirestore, collection, setDoc, doc, addDoc } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-firestore.js"; 
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-analytics.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
  
// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

const firebaseConfig = {
    apiKey: "AIzaSyANWKTp4RFFLTB2DlF6VLD4AwPZbKANJ4c",
    authDomain: "richest-finest-database.firebaseapp.com",
    projectId: "richest-finest-database",
    storageBucket: "richest-finest-database.appspot.com",
    messagingSenderId: "573177601875",
    appId: "1:573177601875:web:7838f564046e9c942dcba6",
    measurementId: "G-WZ156LP4ZM"
};
  

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
  
const db = getFirestore(app);
const dbRef = collection(db, "emails")

function emailIsValid(email) {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
};

async function addEmail(firstName, lastName, email) {
    firstName = firstName.toUpperCase();
    lastName = lastName.toUpperCase();

    if (!emailIsValid(email)) {
        throw new Error("Email is not valid")
    }

    const data = {
        firstName: firstName,
        lastName: lastName,
        email: email
    };

    await addDoc(collection(db, "emails"), data);
}

var subscribeForm = document.getElementById("subscribe-form");

subscribeForm.addEventListener("submit", async function(e) {
    e.preventDefault();

    var firstName = subscribeForm.elements["first-name"].value;
    var lastName = subscribeForm.elements["last-name"].value;
    var email = subscribeForm.elements["email"].value;
    
    try {
        await addEmail(firstName, lastName, email);
        window.location.href = "/subscribe-success.html"
    } catch {
        window.alert("That is not a valid email!")
    }
});