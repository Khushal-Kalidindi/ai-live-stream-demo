import Chat from "@/components/Chat";
import ChatMessage from "@/components/ChatMessage";
import ChatBox from "@/components/ChatBox";
import { Text, View, ActivityIndicator } from "react-native";
import VideoPlayer from "@/components/VideoPlayer";
import StreamDetails from "@/components/StreamDetails";
import React from "react";
import { ScheduledStreamProps } from "@/constants/StreamProps";
import { useRouter } from 'expo-router';
import { useState } from "react";
import { useLocalSearchParams } from "expo-router";
import { useEffect } from "react";
import { Stack } from 'expo-router';

export default function LiveScreen(props: ScheduledStreamProps) {
  const router = useRouter();

  const { stream_id } = useLocalSearchParams(); // Get stream_title from the route params

  const [streamData, setStreamData] = useState(null);

  useEffect(() => {
    // Fetch the stream data based on the stream_title parameter
    const fetchStreamData = async () => {
      console.log("Fetching stream data");
      console.log(stream_id);
      try {
        const response = await fetch(`http://localhost:5000/get_scheduled_stream/${stream_id}`); // Replace with your actual endpoint
        const data = await response.json();
        setStreamData(data);
      } catch (error) {
        console.error('Error fetching stream data:', error);
      }
    };

    if (stream_id) {
      fetchStreamData();
    }
  }, [stream_id]);

  if (!streamData) {
    return <ActivityIndicator size="large" color="#0000ff" />;
  }
  console.log("DATA");
  console.log(streamData);
  return (
    <View
      style={{
        flex: 1
      }}
    >
      <Stack.Screen options={{ header: () => null }} />
      <VideoPlayer flex={1} startTime={30} videoUrl={(streamData as ScheduledStreamProps).video_url}/>
      
      <StreamDetails {...streamData as ScheduledStreamProps}/>
      <Chat flex={3} user_id={window.location.port == "8080" ? "Devin" : "Samantha"} {...streamData as ScheduledStreamProps}/>
    </View>
  );
}