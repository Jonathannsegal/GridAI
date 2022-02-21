import firebase from 'firebase/app';
import 'firebase/auth';
import 'firebase/firestore';
import 'firebase/storage';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

// this is required to fix same-site cors errors
const setCookieSameSite = (res, value) => {
  const cookies = res.getHeader('Set-Cookie');
  res.setHeader('Set-Cookie', cookies?.map((cookie) => cookie.replace('SameSite=Lax', `SameSite=${value}`)));
};

export const preview = async (_req, res) => {
  res.setPreviewData({});
  setCookieSameSite(res, 'None');
};

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

// Auth exports
export const auth = firebase.auth();
export const googleAuthProvider = new firebase.auth.GoogleAuthProvider();

// Firestore exports
export const firestore = firebase.firestore();

// Storage exports
export const storage = firebase.storage();

/// Helper functions

/** `
 * Gets a users/{uid} document with username
 * @param  {string} username
 */
export async function getUserWithUsername(username) {
  const usersRef = firestore.collection('users');
  const query = usersRef.where('username', '==', username).limit(1);
  const userDoc = (await query.get()).docs[0];
  return userDoc;
}

/**
 * 
 * Trying to figure out promises:
 * https://dev.to/ramonak/javascript-how-to-access-the-return-value-of-a-promise-object-1bck
 */
export async function getAllNodes(username){
  // const useruid = firebase.auth().currentUser.uid
  const db = firebase.firestore();
  

  let usersRef = db.collection('users/'+ "ZyZ2MNHXhoW8pupQjHMHVxP4Ed63"+'/nodes');
  let allUsers = await usersRef.get();
  let nodes = allUsers.docs.map(doc=> doc.data());
  console.log("Bad energy type nodes: ", typeof(nodes));
  console.log("Xander's bad energy", nodes);

  // let docs = await users.collection('nodes');
  // console.log("Good energy:", docs)
  // let nodes = users.ref.collection('nodes').get();
  // console.log("Marissa Good Energy nodes: ", nodes);
  // let nodes = [];

  
  //     users.forEach(userDoc => {
  //       userDoc.ref.collection('nodes').get().then(nodesSnapshot => {
  //         nodesSnapshot.forEach(nodesDoc => {
  //           // console.log("Nodes:", nodesDoc.data().id);
  //           let object = {"id":nodesDoc.data().id}
  //           nodes.push(object);
  //         });
  //       });
  //     })
  //   .catch((error) => { 
  //       console.log("Error getting document: ", error);
  //   }); 

  //   console.log("Good energy nodes: ", nodes)
  let nodesArray = [];
  for(var i in nodes)
    nodesArray.push(nodes[i]);
  return nodesArray;
}


