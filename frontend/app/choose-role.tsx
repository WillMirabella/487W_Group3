import { router } from "expo-router";
import { Fragment } from "react";
import { StatusBar, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { colors } from "../constants/colors";
import BigButton from "../components/buttons/big-button";
import SmallButton from "../components/buttons/small-button";

type Role = "driver" | "rider" | "both";

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

      <SafeAreaView
        edges={["left", "right", "bottom"]}
        style={styles.container}
      >
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

            <BigButton
              text="Both"
              onPress={() => chooseRole("both")}
            />
          </View>
        </View>
      </SafeAreaView>
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
    marginTop: 72,
    marginBottom: 40,
  },
  options: {
    gap: 20,
  },
});