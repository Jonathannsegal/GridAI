import dynamic from 'next/dynamic';

const DynamicComponentWithNoSSR = dynamic(() => import('../components/voice'), {
  ssr: false,
});

// eslint-disable-next-line func-names
export default function () {
  return <DynamicComponentWithNoSSR />;
}
