import dynamic from 'next/dynamic';

const DynamicComponentWithNoSSR = dynamic(() => import('./voice'), {
  ssr: false,
});

export default function () {
  return <DynamicComponentWithNoSSR />;
}
