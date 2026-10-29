
import { View, Text, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { colors } from "../../constants/colors";

export default function ProfileScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>My Profile</Text>

      <View style={styles.profileCard}>
        <Text style={styles.avatar}>👤</Text>
        <Text style={styles.name}>Test Student</Text>
        <Text style={styles.email}>abc123@psu.edu</Text>
      </View>

      <View style={styles.infoCard}>
        <Text style={styles.label}>User Type</Text>
        <Text style={styles.value}>Rider</Text>

        <Text style={styles.label}>Campus</Text>
        <Text style={styles.value}>Penn State Abington</Text>

        <Text style={styles.label}>Transportation Preference</Text>
        <Text style={styles.value}>Looking for rides</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: colors.primary,
    marginBottom: 20,
  },
  profileCard: {
    backgroundColor: colors.secondary,
    padding: 25,
    borderRadius: 15,
    alignItems: "center",
    marginBottom: 20,
  },
  avatar: {
    fontSize: 50,
    marginBottom: 10,
  },
  name: {
    fontSize: 22,
    fontWeight: "bold",
    color: colors.background,
  },
  email: {
    fontSize: 16,
    color: colors.accent,
    marginTop: 5,
  },
  infoCard: {
    backgroundColor: "#F5F7FA",
    padding: 20,
    borderRadius: 15,
    borderWidth: 1,
    borderColor: colors.border,
  },
  label: {
    fontSize: 14,
    fontWeight: "bold",
    color: colors.primary,
    marginTop: 15,
  },
  value: {
    fontSize: 16,
    color: colors.secondary,
    marginTop: 5,
  },
});
