import { View } from "react-native";
import { colors } from "../constants/colors";

export default function Divider() {
  return (
    <View style={styles.divider}></View>
  );
}

const styles = {
  divider: {
    height: 2,
    backgroundColor: colors.border,
    marginVertical: 12,
  },
};
