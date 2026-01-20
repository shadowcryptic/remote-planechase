// common.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import {
  getFirestore,
  doc,
  setDoc,
  onSnapshot,
  runTransaction,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyDQcaTRaafEoKNYiTpElLWRa9cfpiP0y5w",
  authDomain: "remote-planechase.firebaseapp.com",
  projectId: "remote-planechase",
  storageBucket: "remote-planechase.firebasestorage.app",
  messagingSenderId: "533208797807",
  appId: "1:533208797807:web:795c57b0fdee32ae05339a"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

export {
  doc,
  setDoc,
  onSnapshot,
  runTransaction,
  serverTimestamp
};
