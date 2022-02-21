/* eslint-disable import/extensions */
/* eslint-disable react/prop-types */
import '../styles/globals.css';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { UserContext } from '../lib/context';
import { useUserData } from '../lib/hooks';

function MyApp({ Component, pageProps }) {
  const userData = useUserData();

  return (
    <UserContext.Provider value={userData}>
      <Navbar />
      <Component {...pageProps} />
      <Footer />
    </UserContext.Provider>
  );
}

export default MyApp;
