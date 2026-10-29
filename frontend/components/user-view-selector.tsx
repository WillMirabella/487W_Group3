import { Pressable, StyleSheet, Text, View } from 'react-native';
import { colors } from '../constants/colors';

type Props = {
  expanded: boolean;
  onChange: (expanded: boolean) => void;
};

// The screen shares this selected view with every user card.
export default function UserViewSelector({ expanded, onChange }: Props) {
  return (
    <View style={styles.buttons}>
      <Pressable
        accessibilityRole="button"
        accessibilityState={{ selected: !expanded }}
        onPress={() => onChange(false)}
        style={[styles.button, !expanded && styles.selectedButton]}
      >
        <Text style={[styles.label, !expanded && styles.selectedLabel]}>Compact</Text>
      </Pressable>
      <Pressable
        accessibilityRole="button"
        accessibilityState={{ selected: expanded }}
        onPress={() => onChange(true)}
        style={[styles.button, expanded && styles.selectedButton]}
      >
        <Text style={[styles.label, expanded && styles.selectedLabel]}>Expanded</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  buttons: { flexDirection: 'row', gap: 12, marginBottom: 16 },
  button: {
    flex: 1,
    minHeight: 44,
    padding: 12,
    borderWidth: 1,
    borderColor: colors.primary,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  selectedButton: { backgroundColor: colors.primary },
  label: { color: colors.primary, fontWeight: '600' },
  selectedLabel: { color: colors.background },
});
