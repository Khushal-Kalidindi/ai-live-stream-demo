import { View, Text } from 'react-native';
import { StyleSheet } from 'react-native';

interface ChatMessageProps {
  username: string;
  message: string;
  usernameColor: string;
  marginBottom?: number;
}

export default function ChatMessage({ username, message, usernameColor, marginBottom = 0}: ChatMessageProps) {
  return (
    <View style={[styles.container, { marginBottom: marginBottom }]}>
      <Text style={[styles.username, { color: usernameColor }]}>{username}</Text>
      <Text style={styles.message}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
    container: {
        padding: 10,
        marginVertical: 5,
        borderRadius: 5,
        backgroundColor: '#f0f0f0',
    },
    username: {
        fontWeight: 'bold',
    },
    message: {
        marginTop: 5,
    },
});