import React, { useState } from 'react';
import { View, Text } from 'react-native';
import YouTube from "react-native-youtube-iframe";
import { YoutubeIframeProps } from 'react-native-youtube-iframe';
const YoutubePlayer = (props: Omit<YoutubeIframeProps, 'height'>) => {
    const [parentHeight, setParentHeight] = useState(0);

    return (
        <View
            onLayout={(event) => {
                setParentHeight(event.nativeEvent.layout.height);
            }}
            style={{ backgroundColor: 'lightblue' }}
        >
            <Text>Parent Height: {parentHeight}</Text>
            {/* <YouTube {...props} height={parentHeight} /> */}
        </View>
    );
};

export default YoutubePlayer;