/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable max-len */
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useContext } from 'react';
import { UserContext } from '../lib/context';
import { auth } from '../lib/firebase';

// Top navbar
export default function Navbar() {
  const { user, username } = useContext(UserContext);

  const router = useRouter();

  const signOut = () => {
    auth.signOut();
    router.reload();
  };
  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'About', href: '/' },
    { name: 'Wiki', href: '/' },
    { name: 'Settings', href: '/' },
  ];

  return (
    <section className="relative w-full px-8 text-gray-700 bg-white body-font">
      <div className="container flex flex-col flex-wrap items-center justify-between py-5 mx-auto md:flex-row max-w-7xl">
        <a href="/" className="relative z-10 flex items-center w-auto text-2xl font-extrabold leading-none text-black select-none">
          grid ai.
        </a>
        <nav className="top-0 left-0 z-0 flex items-center justify-center w-full h-full py-2 -ml-0 space-x-5 text-base md:-ml-5 md:py-0 md:absolute">
          {navigation.map((item) => (
            /* x-data="{ hover: false }" @mouseenter="hover = true" @mouseleave="hover = false" */
            <a href={item.href} key={item.name} className="relative font-medium leading-6 text-gray-600 transition duration-150 ease-out hover:text-gray-900">
              <span className="block">{item.name}</span>
              {/* <span className="absolute bottom-0 left-0 inline-block w-full h-0.5 -mb-1 overflow-hidden">
                    <span x-show="hover" className="absolute inset-0 inline-block w-full h-1 h-full transform bg-gray-900" x-transition:enter="transition ease duration-200" x-transition:enter-start="scale-0" x-transition:enter-end="scale-100" x-transition:leave="transition ease-out duration-300" x-transition:leave-start="scale-100" x-transition:leave-end="scale-0" style="display: none;"></span>
                </span> */}
            </a>
          ))}
        </nav>
        {username ? (
          <div className="relative z-10 inline-flex items-center space-x-3 md:ml-5 lg:justify-end">
            <a onClick={signOut} className="cursor-pointer inline-flex items-center justify-center px-4 py-2 text-base font-medium leading-6 text-gray-600 whitespace-no-wrap bg-white border border-gray-200 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:shadow-none">
              Sign Out
            </a>
            <span className="inline-flex rounded-md shadow-sm">
              <Link href={`/${username}`}>
                <img alt="profile" className="rounded-full w-11 h-11 cursor-pointer" src={user?.photoURL || '/user.png'} />
              </Link>
            </span>
          </div>
        ) : (
          <div className="relative z-10 inline-flex items-center space-x-3 md:ml-5 lg:justify-end">
            <a href="/enter" className="inline-flex items-center justify-center px-4 py-2 text-base font-medium leading-6 text-white whitespace-no-wrap bg-blue-600 border border-blue-700 rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Sign in / Sign up
            </a>
            {/* <span className="inline-flex rounded-md shadow-sm">
              <a href="/enter" className="inline-flex items-center justify-center px-4 py-2 text-base font-medium leading-6 text-gray-600 whitespace-no-wrap bg-white border border-gray-200 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:shadow-none">
                Sign up
              </a>
            </span> */}
          </div>
        )}
      </div>
    </section>
  );
}
