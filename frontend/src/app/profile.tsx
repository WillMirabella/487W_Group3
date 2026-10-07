import Ionicons from '@expo/vector-icons/Ionicons';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

// ProfilePage: your own UserPage, as described in the UML.
export default function ProfilePage() {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.label}>PENN STATE ABINGTON</Text>
      <Text accessibilityRole="header" style={styles.title}>Profile</Text>
      <View style={styles.card}>
        <Ionicons name="person-outline" size={48} color="#1E407C" />
        <Text style={styles.cardTitle}>Coming soon</Text>
        <Text style={styles.description}>Your commuter profile, schedule, and transportation preferences will live here. Profile editing is coming soon.</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { backgroundColor: '#FFFFFF' },
  content: { padding: 24, width: '100%', maxWidth: 640, alignSelf: 'center' },
  label: { color: '#1E407C', fontSize: 11, fontWeight: '700', marginTop: 16 },
  title: { color: '#102A43', fontSize: 32, fontWeight: '700', marginTop: 12, marginBottom: 32 },
  card: {
    backgroundColor: '#F4F8FC',
    borderColor: '#E2E8F0',
    borderWidth: 1,
    borderRadius: 16,
    padding: 32,
    alignItems: 'center',
    gap: 20,
  },
  cardTitle: { color: '#1E407C', fontSize: 20, fontWeight: '600' },
  description: { color: '#526477', fontSize: 16, lineHeight: 25, textAlign: 'center' },
});
