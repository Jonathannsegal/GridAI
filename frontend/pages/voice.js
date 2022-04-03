/* eslint-disable no-unused-vars */
/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable import/extensions */
/* eslint-disable react/prop-types */
import * as React from 'react';
// import Launcher from 'react-chat-window';
import { useEffect } from 'react';
import ChatWidget from '../components/ChatWidget';
import Metatags from '../components/Metatags';
import { sendTextRequest } from '../lib/calls';

export default function Voice() {
  // useEffect(() => {
  //   addResponseMessage('Welcome to this awesome chat!');
  // }, []);

  const handleNewUserMessage = async (newMessage) => {
    const responce = await sendTextRequest(newMessage);
    // eslint-disable-next-line no-console
    console.log(`New message incoming! ${responce}`);
    // Now send the message throught the backend API
  };

  return (
    <main>
      <Metatags title="Grid AI" description="GridAI" />

      <p>welcome to voice</p>

      <ChatWidget
        handleNewUserMessage={handleNewUserMessage}
        title="GridAI"
        subtitle=""
      />

    </main>
  );
}