
import React, { useState } from 'react';
import { View, StyleSheet, Text } from "react-native";
import YouTube from "react-native-youtube-iframe";
import YoutubePlayer from "./YouTubePlayer";

interface VideoPlayerProps {
    flex: number;
    startTime: number;
}
export default function VideoPlayer({ flex, startTime }: VideoPlayerProps) {
  const [parentHeight, setParentHeight] = useState(200);
  const [parentWidth, setParentWidth] = useState(200);
  return (
    <View 
        onLayout={(event) => {
            setParentHeight(event.nativeEvent.layout.height);
            setParentWidth(event.nativeEvent.layout.width);
        }}
        style={[styles.container, {flex: flex}]}>
      {/* <YouTube videoId="VdivYZ3EGsc" width={parentWidth} height={200} play={true}/> */}
      {
        parentWidth/parentHeight > 3 ?
        <iframe src= {`https://www.youtube.com/embed/VdivYZ3EGsc?autoplay=1&showinfo=0&controls=0&mute=1&start=${startTime+4}`}
            frameBorder='0'
            allow='autoplay; encrypted-media'
            allowFullScreen
            height={parentHeight}
            title='video'/>:
        <iframe src= {`https://www.youtube.com/embed/VdivYZ3EGsc?autoplay=1&showinfo=0&controls=0&mute=1&start=${startTime+4}`}
            frameBorder='0'
            allow='autoplay; encrypted-media'
            allowFullScreen
            width={parentWidth}
            height={parentHeight}
            title='video'/>
      }
      <View style={styles.overlay}>
        <Text style={styles.overlayText}>{parentWidth/parentHeight}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: "relative",
    alignItems: "center",
    overflow: "visible",
  },
  overlay: {
    position: "absolute",
    top: 50,
    left: 50,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    padding: 10,
    borderRadius: 10,
  },
  overlayText: {
    color: "white",
    fontSize: 16,
  },
});

