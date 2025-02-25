import React, { useState } from "react";
import { View, TextInput, Button, StyleSheet, Text } from "react-native";
import { TouchableOpacity } from "react-native-gesture-handler";

// Define the type for the props
interface ChatBoxProps {
  sendMessage: (message: string) => void; // Prop to send message
}

export default function ChatBox({ sendMessage }: ChatBoxProps) {
  const [message, setMessage] = useState("");

  const handleSendMessage = () => {
    if (message.trim() !== "") {
      console.log('Message sending1:', message);
      sendMessage(message); // Call the sendMessage prop
      setMessage(""); // Clear the message input after sending
      //Trigger TextInput to clear the input
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Type a message..."
        value={message}
        onChangeText={setMessage}
      />
      <TouchableOpacity style={styles.button} onPress={() => handleSendMessage()}>
          <Text style={styles.buttonText}>Send</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    padding: 10,
    borderTopWidth: 1,
    borderColor: "#ccc",
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 5,
    padding: 10,
    marginRight: 10,
  },
  button: {
    backgroundColor: "#CA442C",
    paddingVertical: 8,
    paddingHorizontal: 15,
    borderRadius: 5,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
  },
});
