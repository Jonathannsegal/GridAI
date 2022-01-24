/* eslint-disable react/prop-types */
import Head from 'next/head';

export default function Metatags({
  title = 'GridAI',
  description = 'GridAI Cloud-based Machine Deep Learning for Power Grid Data Analytics  ',
  image = 'https://git.ece.iastate.edu/uploads/-/system/project/avatar/3874/GridAI_Logo-01.png',
}) {
  return (
    <Head>
      <title>{title}</title>
      <meta name="twitter:card" content="summary" />
      <meta name="twitter:site" content="@gridai" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />

      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />
    </Head>
  );
}
