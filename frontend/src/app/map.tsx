import Ionicons from '@expo/vector-icons/Ionicons';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

// MapDisplay: the planned MapWidget will show location and route information.
export default function MapDisplay() {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.label}>PENN STATE ABINGTON</Text>
      <Text accessibilityRole="header" style={styles.title}>Map</Text>
      <View style={styles.card}>
        <Ionicons name="map-outline" size={48} color="#1E407C" />
        <Text style={styles.cardTitle}>Coming soon</Text>
        <Text style={styles.description}>Explore pickup areas and routes to campus. The interactive map is coming soon.</Text>
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
