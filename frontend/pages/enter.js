/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
/* eslint-disable no-nested-ternary */
/* eslint-disable react/button-has-type */
/* eslint-disable max-len */
/* eslint-disable no-use-before-define */
/* eslint-disable no-console */
/* eslint-disable no-shadow */
/* eslint-disable jsx-a11y/label-has-associated-control */
import * as React from 'react';
import {
  useEffect, useState, useCallback, useContext,
} from 'react';
import debounce from 'lodash.debounce';
import { auth, firestore, googleAuthProvider } from '../lib/firebase';
import { UserContext } from '../lib/context';
import Metatags from '../components/Metatags';

export default function Enter(props) {
  const { user, username } = useContext(UserContext);

  // 1. user signed out <SignInButton />
  // 2. user signed in, but missing username <UsernameForm />
  // 3. user signed in, has username <SignOutButton />
  return (
    <main>
      <Metatags title="Enter" description="Sign up for this amazing app!" />

      {user ? !username ? <UsernameForm /> : <SignOutButton /> : <SignInButton />}
    </main>
  );
}

// Sign in with Google button
function SignInButton() {
  const signInWithGoogle = async () => {
    await auth.signInWithPopup(googleAuthProvider);
  };

  return (
    <>
      <section className="w-full bg-white">

        <div className="mx-auto max-w-7xl">
          <div className="flex flex-col lg:flex-row">
            <div className="relative w-full bg-cover lg:w-6/12 xl:w-7/12 bg-gradient-to-r from-white via-white to-gray-100">
              <div className="relative flex flex-col items-center justify-center w-full h-full px-10 my-20 lg:px-16 lg:my-0">
                <div className="flex flex-col items-start space-y-8 tracking-tight lg:max-w-3xl">
                  <div className="relative">
                    <p className="mb-2 font-medium text-gray-700 uppercase">Work smarter</p>
                    <h2 className="text-5xl font-bold text-gray-900 xl:text-6xl">Features to help you work smarter</h2>
                  </div>
                  <p className="text-2xl text-gray-700">We&apos;ve created a simple formula to follow in order to gain more out of your business and your application.</p>
                  <a href="#_" className="inline-block px-8 py-5 text-xl font-medium text-center text-white transition duration-200 bg-blue-600 rounded-lg hover:bg-blue-700 ease">Get Started Today</a>
                </div>
              </div>
            </div>

            <div className="w-full bg-white lg:w-6/12 xl:w-5/12">
              <div className="flex flex-col items-start justify-start w-full h-full p-10 lg:p-16 xl:p-24">
                <h4 className="w-full text-3xl font-bold">Signup</h4>
                <p className="text-lg text-gray-500">
                  or, if you have an account you can
                  {' '}
                  <a href="#_" className="text-blue-600 underline">sign in</a>
                </p>
                <div className="relative w-full mt-10 space-y-8">
                  <div className="relative">
                    <label className="font-medium text-gray-900">Name</label>
                    <input type="text" className="block w-full px-4 py-4 mt-2 text-xl placeholder-gray-400 bg-gray-200 rounded-lg focus:outline-none focus:ring-4 focus:ring-blue-600 focus:ring-opacity-50" placeholder="Enter Your Name" />
                  </div>
                  <div className="relative">
                    <label className="font-medium text-gray-900">Email</label>
                    <input type="text" className="block w-full px-4 py-4 mt-2 text-xl placeholder-gray-400 bg-gray-200 rounded-lg focus:outline-none focus:ring-4 focus:ring-blue-600 focus:ring-opacity-50" placeholder="Enter Your Email Address" />
                  </div>
                  <div className="relative">
                    <label className="font-medium text-gray-900">Password</label>
                    <input type="password" className="block w-full px-4 py-4 mt-2 text-xl placeholder-gray-400 bg-gray-200 rounded-lg focus:outline-none focus:ring-4 focus:ring-blue-600 focus:ring-opacity-50" placeholder="Password" />
                  </div>
                  <div className="relative">
                    <a href="#_" className="inline-block w-full px-5 py-4 text-lg font-medium text-center text-white transition duration-200 bg-blue-600 rounded-lg hover:bg-blue-700 ease">Create Account</a>
                    <button onClick={signInWithGoogle} className="inline-block w-full px-5 py-4 mt-3 text-lg font-bold text-center text-gray-900 transition duration-200 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 ease">
                      Sign up with Google
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </section>
      {/* <button className="btn-google" onClick={signInWithGoogle}>
        Sign in with Google
      </button>
      <button onClick={() => auth.signInAnonymously()}>
        Sign in Anonymously
      </button> */}
    </>
  );
}

// Sign out button
function SignOutButton() {
  return <button onClick={() => auth.signOut()}>Sign Out</button>;
}

// Username form
function UsernameForm() {
  const [formValue, setFormValue] = useState('');
  const [isValid, setIsValid] = useState(false);
  const [loading, setLoading] = useState(false);

  const { user, username } = useContext(UserContext);

  const onSubmit = async (e) => {
    e.preventDefault();

    // Create refs for both documents
    const userDoc = firestore.doc(`users/${user.uid}`);
    const usernameDoc = firestore.doc(`usernames/${formValue}`);

    // Commit both docs together as a batch write.
    const batch = firestore.batch();
    batch.set(userDoc, { username: formValue, photoURL: user.photoURL, displayName: user.displayName });
    batch.set(usernameDoc, { uid: user.uid });

    await batch.commit();
  };

  const onChange = (e) => {
    // Force form value typed in form to match correct format
    const val = e.target.value.toLowerCase();
    const re = /^(?=[a-zA-Z0-9._]{3,15}$)(?!.*[_.]{2})[^_.].*[^_.]$/;

    // Only set form value if length is < 3 OR it passes regex
    if (val.length < 3) {
      setFormValue(val);
      setLoading(false);
      setIsValid(false);
    }

    if (re.test(val)) {
      setFormValue(val);
      setLoading(true);
      setIsValid(false);
    }
  };

  //

  useEffect(() => {
    checkUsername(formValue);
  }, [formValue]);

  // Hit the database for username match after each debounced change
  // useCallback is required for debounce to work
  const checkUsername = useCallback(
    debounce(async (username) => {
      if (username.length >= 3) {
        const ref = firestore.doc(`usernames/${username}`);
        const { exists } = await ref.get();
        console.log('Firestore read executed!');
        setIsValid(!exists);
        setLoading(false);
      }
    }, 500),
    [],
  );

  return (
    !username && (
      <section>
        <h3>Choose Username</h3>
        <form onSubmit={onSubmit}>
          <input name="username" placeholder="myname" value={formValue} onChange={onChange} />
          <UsernameMessage username={formValue} isValid={isValid} loading={loading} />
          <button type="submit" className="btn-green" disabled={!isValid}>
            Choose
          </button>

          <h3>Debug State</h3>
          <div>
            Username:
            {' '}
            {formValue}
            <br />
            Loading:
            {' '}
            {loading.toString()}
            <br />
            Username Valid:
            {' '}
            {isValid.toString()}
          </div>
        </form>
      </section>
    )
  );
}

function UsernameMessage({ username, isValid, loading }) {
  if (loading) {
    return <p>Checking...</p>;
  } if (isValid) {
    return (
      <p className="text-success">
        {username}
        {' '}
        is available!
      </p>
    );
  } if (username && !isValid) {
    return <p className="text-danger">That username is taken!</p>;
  }
  return <p />;
}
