import Chat from "@/components/Chat";
import ChatMessage from "@/components/ChatMessage";
import ChatBox from "@/components/ChatBox";
import { Text, View } from "react-native";
import VideoPlayer from "@/components/VideoPlayer";
import React from "react";


//Dummy chat messages


export default function Index() {
  return (
    <View
      style={{
        flex: 1
      }}
    >
      <VideoPlayer flex={1} startTime={30}/>
      <Chat flex={3} user_id={window.location.port}/>
    </View>
  );
}
