import { StyleSheet } from 'react-native';

// Shared appearance for the placeholder screens.
export const screenStyles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#FFFFFF' },
  content: { padding: 24, width: '100%', maxWidth: 640, alignSelf: 'center' },
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
