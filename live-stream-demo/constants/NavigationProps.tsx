import { ScheduledStreamProps } from "./StreamProps";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
// Define types for the navigation
export type RootStackParamList = {
  StreamList: undefined;
  LiveScreen: ScheduledStreamProps;
};
