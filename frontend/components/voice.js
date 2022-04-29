/* eslint-disable react/no-this-in-sfc */
/* eslint-disable no-unused-vars */
/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable import/extensions */
/* eslint-disable react/prop-types */
import React, { useState, useEffect } from 'react';
// import Launcher from 'react-chat-window';
// import { useEffect } from 'react';
import { Widget, addResponseMessage } from 'react-chat-widget';
// import { Recorder } from 'react-voice-recorder';
// import ChatWidget from './ChatWidget';
import Metatags from './Metatags';
import { sendTextRequest } from '../lib/calls';
// import 'react-voice-recorder/dist/index.css';

export default function Voice() {
  // eslint-disable-next-line react/no-this-in-sfc
  // this.state = {
  //   audioDetails: {
  //     url: null,
  //     blob: null,
  //     chunks: null,
  //     duration: {
  //       h: 0,
  //       m: 0,
  //       s: 0,
  //     },
  //   },
  // };
  const handleAudioStop = (data) => {
    this.setState({ audioDetails: data });
  };

  // useEffect(() => {
  //   addResponseMessage('Welcome to this awesome chat!');
  // }, []);

  const handleNewUserMessage = async (newMessage) => {
    const responce = await sendTextRequest(newMessage);
    // eslint-disable-next-line no-console
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
      {/* <Recorder
        record
        title="New recording"
        // audioURL={this.state.audioDetails.url}
        showUIAudio
        handleAudioStop={(data) => this.handleAudioStop(data)}
        handleAudioUpload={(data) => this.handleAudioUpload(data)}
        handleCountDown={(data) => this.handleCountDown(data)}
        handleReset={() => this.handleReset()}
        mimeTypeToUseWhenRecording="audio/webm"
      /> */}

    </main>
  );
}
