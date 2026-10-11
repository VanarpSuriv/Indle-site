import {initializeApp} from 'https://www.gstatic.com/firebasejs/12.4.0/firebase-app.js';
import {getAuth, GoogleAuthProvider, inMemoryPersistence, setPersistence, signInWithPopup,
  reauthenticateWithPopup, deleteUser, signOut} from 'https://www.gstatic.com/firebasejs/12.4.0/firebase-auth.js';
import {deleteVerifiedAccount} from './delete-flow.mjs';

const status = document.querySelector('#status');
const signInButton = document.querySelector('#sign-in');
const deleteButton = document.querySelector('#delete-account');
const confirmation = document.querySelector('#confirm');
const form = document.querySelector('#deletion-form');
let auth;
let busy = true;
const provider = new GoogleAuthProvider();
provider.setCustomParameters({prompt: 'select_account'});

function controls() {
  signInButton.disabled = busy;
  deleteButton.disabled = busy || !auth?.currentUser || !confirmation.checked;
}

async function configure() {
  if (auth) return auth;
  const response = await fetch('./firebase-public-config.json',
    {cache: 'no-store', signal: AbortSignal.timeout(15000)});
  if (!response.ok) throw new Error('CONFIGURATION_UNAVAILABLE');
  const config = await response.json();
  if (config.projectId !== 'indicgame' || config.authDomain !== 'indicgame.firebaseapp.com' || !config.apiKey) {
    throw new Error('CONFIGURATION_UNAVAILABLE');
  }
  auth = getAuth(initializeApp(config));
  await setPersistence(auth, inMemoryPersistence);
  return auth;
}

signInButton.addEventListener('click', async () => {
  busy = true; controls(); status.textContent = 'Opening Google sign-in…';
  try {
    const credential = await signInWithPopup(await configure(), provider);
    document.querySelector('#account').textContent = credential.user.email ?? 'Your signed-in Google account';
    form.hidden = false;
    status.textContent = 'Review the account shown below before deleting.';
  } catch (error) {
    status.textContent = error?.code === 'auth/unauthorized-domain'
      ? 'Google sign-in has not been enabled for this website. Use the in-app deletion action while the publisher completes configuration.'
      : 'Sign-in could not finish. Check your connection and allow the Google sign-in window.';
  } finally {
    busy = false; controls();
  }
});
confirmation.addEventListener('change', controls);
form.addEventListener('submit', async event => {
  event.preventDefault();
  if (busy || !auth?.currentUser || !confirmation.checked) return;
  busy = true; controls(); status.textContent = 'Verifying ownership and deleting…';
  try {
    await deleteVerifiedAccount(auth.currentUser, {
      reauthenticate: user => reauthenticateWithPopup(user, provider),
      deleteCloud: async token => {
        const response = await fetch('https://hdvmxywtuufejwozgsjv.supabase.co/functions/v1/indle-api', {
          method: 'POST', headers: {'Content-Type': 'application/json', Authorization: `Bearer ${token}`},
          body: JSON.stringify({action: 'deleteAccountData', data: {}}),
          cache: 'no-store', signal: AbortSignal.timeout(30000),
        });
        if (!response.ok) throw new Error('CLOUD_DELETION_NOT_CONFIRMED');
        return response.json();
      },
      deleteIdentity: deleteUser,
      clearSession: () => signOut(auth),
    });
    status.textContent = 'Your Indle cloud records and Firebase account have been deleted.';
    confirmation.checked = false; form.hidden = true;
  } catch (error) {
    status.textContent = error?.message === 'IDENTITY_DELETION_INCOMPLETE'
      ? 'Your cloud records were removed, but account deletion did not finish. Sign in again and retry deletion.'
      : 'Deletion did not finish. No success is recorded. Check your connection and try again.';
  } finally {
    busy = false; controls();
  }
});
controls();
configure().catch(() => {
  status.textContent = 'Sign-in configuration could not load. Check your connection and retry signing in.';
}).finally(() => { busy = false; controls(); });
