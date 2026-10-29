import { router } from "expo-router";
import { Fragment } from "react";
import { StatusBar, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { colors } from "../constants/colors";
import BigButton from "../components/buttons/big-button";

type Role = "driver" | "rider";

export default function ChooseRoleScreen() {
  function chooseRole(role: Role) {
    router.push({
      pathname: "/create-profile",
      params: { role },
    });
  }

    return (
    <Fragment>
      <StatusBar
        barStyle="light-content"
        backgroundColor={colors.secondary}
      />

      <SafeAreaView
        style={{ flex: 0, backgroundColor: colors.secondary }}
      />

      <View style={styles.container}>
        <View style={styles.sheet}>
          <Text style={styles.heading}>
            How would you like to use LionLift?
          </Text>

          <View style={styles.options}>
            <BigButton
              text="Driver"
              onPress={() => chooseRole("driver")}
            />

            <BigButton
              text="Rider"
              onPress={() => chooseRole("rider")}
            />

          </View>
        </View>
      </View>
    </Fragment>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.secondary,
  },
  sheet: {
    flex: 1,
    backgroundColor: colors.background,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingHorizontal: 24,
    paddingBottom: 32,
  },
  heading: {
    color: colors.primary,
    fontSize: 32,
    fontWeight: "bold",
    marginVertical: 24,
  },
  options: {
    gap: 20,
  },
});