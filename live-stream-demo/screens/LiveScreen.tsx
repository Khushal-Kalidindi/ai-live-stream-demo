import Chat from "@/components/Chat";
import ChatMessage from "@/components/ChatMessage";
import ChatBox from "@/components/ChatBox";
import { Text, View } from "react-native";
import VideoPlayer from "@/components/VideoPlayer";
import StreamDetails from "@/components/StreamDetails";
import React from "react";
import { ScheduledStreamProps } from "@/constants/StreamProps";


export default function LiveScreen(props: ScheduledStreamProps) {
  return (
    <View
      style={{
        flex: 1
      }}
    >
      <VideoPlayer flex={1} startTime={30}/>
      <StreamDetails {...props}/>
      <Chat flex={3} user_id={window.location.port}/>
    </View>
  );
}