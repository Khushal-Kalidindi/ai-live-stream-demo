import React, { useState, useEffect, useRef} from 'react';
import { FlatList, View, StyleSheet, ScrollView } from 'react-native';
import ChatMessage from './ChatMessage';
import ChatBox from './ChatBox';
import io from 'socket.io-client';
import { ScheduledStreamProps } from '@/constants/StreamProps';

interface ChatProps {
    flex: number;
    user_id: string;
}

interface Message {
    username: string;
    message: string;
    usernameColor: string;
}

const socket = io('http://localhost:5000');


export default function Chat({ flex = 1, user_id, streamer_name, stream_title }: ChatProps & ScheduledStreamProps) {
const [messages, setMessages] = useState<Message[]>([
    {   
        username: user_id,
        message: 'Hello',  
        usernameColor: '#000',
    }
]);
  const [username, setUsername] = useState(user_id);
  const flatListRef = useRef<FlatList<any>>(null);
  const sendMessage = ( message: String) => {
        console.log('Message sending2:', message);
        if (username && message) {
            const msgData = {
                streamer_name,
                stream_title,
                username,
                message,
                usernameColor: '#000000', // Default color
            };
            console.log('Message sending:', msgData);
            socket.emit('send_message', msgData);
            console.log('Message sent');
        }
        if (flatListRef.current) {
            flatListRef.current.scrollToEnd({ animated: true });
        }
    };

    useEffect(() => {
        const joinStream = async () => {
          try {
            const response = await fetch("http://localhost:5000/join_stream", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ username , streamer_name, stream_title }),
            });
      
            const data = await response.text();
            console.log("Join stream response:", data);
          } catch (error) {
            console.error("Error joining stream:", error);
          }
        };
      
        joinStream();
      }, []);

    // Fetch previous messages when component mounts
    useEffect(() => {
        socket.emit('load_messages');

        socket.on('load_previous_messages', (data) => {
            console.log("Loading messages", data);
            setMessages(data);
            if (flatListRef.current) {
                flatListRef.current.scrollToEnd({ animated: true });
            }
        });

        socket.on('receive_message', (newMessage) => {
            console.log("Received message:", newMessage);
            setMessages((prevMessages) => {
                console.log("Previous messages:", prevMessages);
                if (typeof newMessage === 'string') {
                    newMessage = JSON.parse(newMessage);
                }
                return [...prevMessages, newMessage];
            });
            if (flatListRef.current) {
                flatListRef.current.scrollToEnd({ animated: true });
            }
        });
        

        return () => {
            socket.off('load_previous_messages');
            socket.off('receive_message');
        };
    }, []);
    
  return (
    console.log(messages + typeof(messages)),
    <View style={[styles.container, {flex: flex}]}>
        <FlatList
            ref={flatListRef}  // Set the reference here
            data={messages}
            renderItem={({ item, index }) => (
                <ChatMessage
                    username={item.username}
                    message={item.message}
                    usernameColor={item.usernameColor}
                    marginBottom={index === messages.length - 1 ? 60 : 0}
                />
            )}
            keyExtractor={(item, index) => index.toString()}
            inverted={false}  // Prevents list from being flipped upside down
        />
      <ChatBox sendMessage={sendMessage} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 10,
  },
});
