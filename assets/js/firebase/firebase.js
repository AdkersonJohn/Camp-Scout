// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA-TDCiGHP0jiCunMFhb0YrtomkVPggN-4",
  authDomain: "camp-scout.firebaseapp.com",
  projectId: "camp-scout",
  storageBucket: "camp-scout.appspot.com",
  messagingSenderId: "533142929085",
  appId: "1:533142929085:web:b4748223c0f1f0613301d4",
  measurementId: "G-Y6H2X0XNDM",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

const auth = getAuth();
signInWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // Signed in
    const user = userCredential.user;
    // ...
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
  });

export { signInWithEmailAndPassword };
