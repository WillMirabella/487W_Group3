import { Pressable, StyleSheet, Text } from "react-native";
import { colors } from "../../constants/colors";

type Props = {
  text: string;
  onPress: () => void;
  borderOnly?: boolean;
};

export default function BigButton({ text, onPress, borderOnly }: Props) {
  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      style={({ pressed }) => [
        styles(borderOnly).button,
        pressed && styles(borderOnly).buttonPressed,
      ]}
    >
      <Text style={styles(borderOnly).text}>{text}</Text>
    </Pressable>
  );
}

const styles = (borderOnly: boolean | undefined) => StyleSheet.create({
  button: {
    backgroundColor: (borderOnly ?? false) ? "transparent" : colors.secondary,
    borderWidth: (borderOnly ?? false) ? 2 : 0,
    borderColor: colors.secondary,
    paddingVertical: 16,
    paddingHorizontal: 12,
    borderRadius: 16,
    marginVertical: 12,
  },
  buttonPressed: {
    backgroundColor: colors.accent,
  },
  text: {
    color: (borderOnly ?? false) ? colors.secondary : colors.background,
    fontSize: 16,
    fontWeight: "bold",
    textAlign: "center",
  },
});
