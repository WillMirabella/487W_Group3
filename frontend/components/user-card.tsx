/*
 * Component for the user card that will be displayed in the "market place"
 * This should be able to showcase the pfp of the user but also have a fallback
 * in case they do not have one. Maybe the fallback should be on the user profile side.
 */

import { View, StyleSheet, Text } from "react-native";
import { colors } from "../constants/colors";

type Props = {
  expanded?: boolean;
};

export default function UserCard({ expanded=false }: Props) {
  return (
    <View style={styles.card} accessibilityRole="button">
        <View style={{ flexDirection: "row" }} accessibilityRole="button">
            <View style={styles.profilePicture}/>
            <View>
                <Text style={styles.heading}>Alex Hanna</Text>

                {/* This is extremely temporary and I am not completely sure what should go here and how it should be displayed */}
                <Text style={styles.subheading}>2 miles away</Text>
                <Text style={styles.subheading}>Male</Text>
                <Text style={styles.subheading}>Driver</Text>
            </View>
        </View>
        {expanded && <View style={styles.map}></View>}
        
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.background,
    borderWidth: 0,
    borderColor: colors.secondary,
    padding: 16,
    borderRadius: 24,
    marginVertical: 12,

    // shadow
    shadowColor: "black",
    shadowRadius: 2,
    shadowOffset: {
        width: 0,
        height: 0
    },
    shadowOpacity: .20
  },
  profilePicture: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: colors.border,
    marginRight: 16
  },
  map: {
    minHeight: 300,
    borderRadius: 8,
    marginTop: 16,
    backgroundColor: colors.border,
  },
  heading: {
    fontSize: 24,
    fontWeight: "bold",
    color: colors.primary
  },
  subheading: {
    fontSize: 18,
    color: colors.primary
  }
});

