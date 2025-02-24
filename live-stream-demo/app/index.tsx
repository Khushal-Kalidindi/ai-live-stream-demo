import { useRouter } from 'expo-router';
import { ScheduledStreamProps } from '@/constants/StreamProps';
import { View, Text, TouchableOpacity } from 'react-native';
import React, { useEffect, useState } from 'react';
import StreamDetails from '@/components/StreamDetails';
const StreamListScreen = () => {
  const [streams, setStreams] = useState([]);
  const router = useRouter();

  useEffect(() => {
    // Fetch scheduled streams from localhost:5000
    const fetchStreams = async () => {
      try {
        const response = await fetch('http://localhost:5000/get_scheduled_streams'); // Replace with your API endpoint
        const data = await response.json();
        setStreams(data['scheduled_streams']);  // Store the data in the state
      } catch (error) {
        console.error('Error fetching streams:', error);
      }
    };

    fetchStreams();
  }, []);

  const navigateToLiveScreen = (stream: ScheduledStreamProps) => {
    router.push({
      pathname: '/live/[stream_id]',  // Use this dynamic route
      params: { stream_id: stream._id }, // Pass the stream title and the whole stream object
    });
  };

  return (
    console.log(streams),
    console.log(typeof streams),
    <View>
      {streams.map((stream: ScheduledStreamProps) => (
        <TouchableOpacity key={stream._id} onPress={() => navigateToLiveScreen(stream as ScheduledStreamProps)}>
          <StreamDetails {...stream} />
        </TouchableOpacity>
      ))}
    </View>
  );
};

export default StreamListScreen;
