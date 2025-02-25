import React, { useState } from "react";
import { View, Text, Image, Button, StyleSheet, TouchableOpacity, RootTagContext } from "react-native";
import { ScheduledStreamProps } from "@/constants/StreamProps";

export default function StreamDetails(props: ScheduledStreamProps) {
  const [isFollowing, setIsFollowing] = useState(false);

  const toggleFollow = () => {
    setIsFollowing(!isFollowing);
  };

  return (
    <View style={styles.container}>
      {/* Profile Picture */}
      <Image 
        source={require("../assets/images/pikachu-pokemon-still.gif")}
        style={styles.profilePic} 
      />

      {/* Title */}
        <View style={styles.detailsContainer}>
            <Text style={styles.title}>{props.stream_title}</Text>
            <Text>{props.stream_description}</Text>
            {/* Tags */}
            <View style={{ flexDirection: "row", marginTop: 5 }}>
                {props.tags.map((tag, index) => (  
                    <View key={index} style={styles.tag}>
                        <Text>{tag}</Text>
                    </View>
                ))}
            </View>

        </View>

      {/* Follow Button */}
        <View style={{ flex: 1, alignItems: "flex-end" }}>
            <TouchableOpacity style={styles.button} onPress={toggleFollow}>
                <Text style={styles.buttonText}>{isFollowing ? "Following" : "Follow"}</Text>
            </TouchableOpacity>
        </View>
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
  detailsContainer: {
    flexDirection: "column",
    alignItems: "flex-start",
    padding: 10,
  },
  tag: {
    backgroundColor: "#f0f0f0",
    padding: 5,
    borderRadius: 5,
    marginRight: 5,
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
