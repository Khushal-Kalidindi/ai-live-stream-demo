import React, { useState } from "react";
import { View, Text, Image, Button, StyleSheet, TouchableOpacity } from "react-native";

export default function StreamDetails() {
  const [isFollowing, setIsFollowing] = useState(false);

  const toggleFollow = () => {
    setIsFollowing(!isFollowing);
  };

  return (
    <View style={styles.container}>
      {/* Profile Picture */}
      <Image 
        source={{ uri: "https://via.placeholder.com/50" }} 
        style={styles.profilePic} 
      />

      {/* Title */}
      <Text style={styles.title}>Stream Title</Text>

      {/* Follow Button */}
      <TouchableOpacity style={styles.button} onPress={toggleFollow}>
        <Text style={styles.buttonText}>{isFollowing ? "Following" : "Follow"}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    padding: 10,
    backgroundColor: "#fff",
  },
  profilePic: {
    width: 50,
    height: 50,
    borderRadius: 25,
    marginRight: 10,
  },
  title: {
    flex: 1,
    fontSize: 16,
    fontWeight: "bold",
  },
  button: {
    backgroundColor: "#007bff",
    paddingVertical: 8,
    paddingHorizontal: 15,
    borderRadius: 5,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
  },
});
