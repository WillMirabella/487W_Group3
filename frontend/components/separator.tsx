import { View } from "react-native";
import { colors } from "../constants/colors";

export default function Separator() {
  return (
    <View >
        <View style={styles.separator}></View>
    </View>
  );
}

const styles = {
  separator: {
    height: 6,
    width: 6,
    borderRadius: 4,
    backgroundColor: colors.secondary,
    marginVertical: 4,
  },
};
