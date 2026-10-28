import { StyleSheet, Text, View } from "react-native";
import { colors } from "../constants/colors";

type Props = {
  children: string;
  fontSize: number;
};

export default function ContainedText({
  children,
  fontSize,
}: Props){
    return (
    <View style={styles(fontSize).container}>
        <Text style={styles(fontSize).text}>{children}</Text>
    </View>
  );
}

const styles = (fontSize: number) => StyleSheet.create({
  container: {
    backgroundColor: colors.accent,
    paddingHorizontal: (fontSize / 2) + 4,
    paddingVertical: 2,
    borderRadius: (fontSize / 2) + 4,
    alignSelf: 'flex-start',
  },
  text: {
    fontSize: fontSize,
    color: colors.primary,
    fontWeight: "500"
  }
});
