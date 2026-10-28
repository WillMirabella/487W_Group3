
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { colors } from "../../constants/colors";

type Ride = {
  id: number;
  driver: string;
  destination: string;
  departure_time: string;
  seats_available: number;
  price: number;
};

export default function FindDriversScreen() {
  const [rides, setRides] = useState<Ride[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRides() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/rides/");

        if (!response.ok) {
          throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();
        setRides(data.rides);
      } catch (err) {
        console.error("Failed to load rides:", err);
        setError("Could not load rides. Please try again.");
      } finally {
        setLoading(false);
      }
    }

    loadRides();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Find Drivers</Text>
        <Text style={styles.subtitle}>
          Find a ride with fellow Penn State Abington commuters.
        </Text>
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={styles.message}>Finding available rides...</Text>
        </View>
      ) : error ? (
        <View style={styles.center}>
          <Text style={styles.error}>{error}</Text>
        </View>
      ) : rides.length === 0 ? (
        <View style={styles.center}>
          <Text style={styles.message}>No rides available right now.</Text>
        </View>
      ) : (
        <FlatList
          data={rides}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={styles.list}
          ListHeaderComponent={
            <Text style={styles.results}>
              {rides.length} rides available
            </Text>
          }
          renderItem={({ item }) => (
            <View style={styles.card}>
              <View style={styles.cardHeader}>
                <View style={styles.driverInfo}>
                  <Text style={styles.driverLabel}>DRIVER</Text>
                  <Text style={styles.driver}>{item.driver}</Text>
                </View>

                <Text style={styles.price}>
                  ${item.price.toFixed(2)}
                </Text>
              </View>

              <View style={styles.divider} />

              <Text style={styles.destinationLabel}>DESTINATION</Text>
              <Text style={styles.destination}>{item.destination}</Text>

              <View style={styles.details}>
                <View>
                  <Text style={styles.detailLabel}>Departure</Text>
                  <Text style={styles.detailValue}>
                    {item.departure_time}
                  </Text>
                </View>

                <View>
                  <Text style={styles.detailLabel}>Available seats</Text>
                  <Text style={styles.detailValue}>
                    {item.seats_available}
                  </Text>
                </View>
              </View>
            </View>
          )}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 16,
  },
  title: {
    fontSize: 30,
    fontWeight: "bold",
    color: colors.primary,
  },
  subtitle: {
    fontSize: 15,
    color: "#666666",
    marginTop: 6,
    lineHeight: 22,
  },
  list: {
    paddingHorizontal: 16,
    paddingBottom: 24,
  },
  results: {
    fontSize: 14,
    color: "#666666",
    marginBottom: 12,
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 14,
    padding: 18,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: "#E3E3E3",
  },
  cardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  driverInfo: {
    flex: 1,
  },
  driverLabel: {
    fontSize: 11,
    fontWeight: "700",
    color: "#777777",
    letterSpacing: 1,
  },
  driver: {
    fontSize: 18,
    fontWeight: "600",
    color: colors.primary,
    marginTop: 4,
  },
  price: {
    fontSize: 20,
    fontWeight: "bold",
    color: colors.primary,
    marginLeft: 12,
  },
  divider: {
    height: 1,
    backgroundColor: "#EAEAEA",
    marginVertical: 16,
  },
  destinationLabel: {
    fontSize: 11,
    fontWeight: "700",
    color: "#777777",
    letterSpacing: 1,
  },
  destination: {
    fontSize: 17,
    fontWeight: "600",
    color: "#222222",
    marginTop: 5,
  },
  details: {
    flexDirection: "row",
    gap: 36,
    marginTop: 18,
  },
  detailLabel: {
    fontSize: 12,
    color: "#777777",
  },
  detailValue: {
    fontSize: 15,
    fontWeight: "600",
    color: "#222222",
    marginTop: 5,
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
  },
  message: {
    color: "#666666",
    fontSize: 15,
    marginTop: 12,
    textAlign: "center",
  },
  error: {
    color: "#B00020",
    fontSize: 15,
    textAlign: "center",
  },
});
