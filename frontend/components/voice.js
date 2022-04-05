/* eslint-disable no-unused-vars */
/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable import/extensions */
/* eslint-disable react/prop-types */
import * as React from 'react';
// import Launcher from 'react-chat-window';
import { useEffect } from 'react';
import { Widget, addResponseMessage } from 'react-chat-widget';
import ChatWidget from './ChatWidget';
import Metatags from './Metatags';
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
    addResponseMessage(`${responce}`);
  };

  return (
    <main>
      <Metatags title="Grid AI" description="GridAI" />

      <p>welcome to voice</p>

      <Widget
        handleNewUserMessage={handleNewUserMessage}
        title="GridAI"
        subtitle=""
      />

    </main>
  );
}
