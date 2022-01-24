/* eslint-disable react/button-has-type */
/* eslint-disable jsx-a11y/iframe-has-title */
import Link from 'next/link';

export default function Custom404() {
  return (
    <main>
      <h1>404 - That page does not seem to exist...</h1>
      <iframe
        src="https://giphy.com/embed/l2JehQ2GitHGdVG9y"
        width="480"
        height="362"
        frameBorder="0"
        allowFullScreen
      />
      <Link href="/">
        <button className="btn-blue">Go home</button>
      </Link>
    </main>
  );
}
