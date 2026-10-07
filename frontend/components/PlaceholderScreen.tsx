import Ionicons from '@expo/vector-icons/Ionicons';
import { type ComponentProps } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

type Props = {
  title: string;
  description: string;
  icon: ComponentProps<typeof Ionicons>['name'];
};

// Shared presentation only; each route can be replaced independently later.
export default function PlaceholderScreen({ title, description, icon }: Props) {
  return (
    <SafeAreaView style={styles.screen} edges={['left', 'right']}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.eyebrow}>PENN STATE ABINGTON</Text>
        <Text accessibilityRole="header" style={styles.title}>{title}</Text>
        <View style={styles.card}>
          <View style={styles.icon} accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
            <Ionicons name={icon} color="#1E407C" size={40} />
          </View>
          <Text style={styles.comingSoon}>Coming soon</Text>
          <Text style={styles.description}>{description}</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#FFFFFF' },
  content: { flexGrow: 1, padding: 24, gap: 12, width: '100%', maxWidth: 640, alignSelf: 'center' },
  eyebrow: { color: '#1E407C', fontSize: 11, fontWeight: '700', letterSpacing: 1.5, marginTop: 16 },
  title: { color: '#102A43', fontSize: 32, fontWeight: '700', marginBottom: 20 },
  card: { alignItems: 'center', backgroundColor: '#F4F8FC', borderColor: '#E2E8F0', borderWidth: 1, borderRadius: 16, paddingHorizontal: 24, paddingVertical: 40, gap: 16 },
  icon: { backgroundColor: '#E5EEFA', borderRadius: 40, padding: 20 },
  comingSoon: { color: '#1E407C', fontSize: 20, fontWeight: '600' },
  description: { color: '#526477', fontSize: 16, lineHeight: 25, textAlign: 'center', maxWidth: 360 },
});
