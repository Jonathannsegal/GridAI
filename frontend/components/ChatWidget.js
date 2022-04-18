import React from 'react';
import dynamic from 'next/dynamic';

const ChatWidget = dynamic(() => import('react-chat-widget').then((mod) => mod.Widget), {
  loading: () => <>Loading&nbsp;&hellip;</>,
  ssr: false,
});
export default ChatWidget;
