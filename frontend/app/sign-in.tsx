import { router } from "expo-router/build/global-state/router";
import { Fragment, useState } from "react";
import {
  Alert,
  Platform,
  StatusBar,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { colors } from "../constants/colors";
import CustomTextInput from "../components/custom-text-input";
import BigButton from "../components/buttons/big-button";
import SmallButton from "../components/buttons/small-button";
import Divider from "../components/divider";
import { KeyboardAvoidingView } from "react-native";

export default function SignInScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [apiMessage, setApiMessage] = useState("Not tested yet");
  const [apiLoading, setApiLoading] = useState(false);

  async function testBackend() {
    setApiLoading(true);
    setApiMessage("Connecting to backend...");

    try {
      const response = await fetch("http://127.0.0.1:5000/api/example/");
      const data = await response.json();

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      setApiMessage(
        data.exampleData ?? "Connected, but response was unexpected",
      );
    } catch (error) {
      console.error("Backend test failed:", error);
      setApiMessage("Connection failed. Check the browser console.");
    } finally {
      setApiLoading(false);
    }
  }

  function handleSignIn() {
    // Temporary redirect for demonstration until authentication is implemented.
    router.replace("/(app)/find-drivers");

    // Authentication validation will be implemented later.
  }

  return (
    <Fragment>
      <StatusBar barStyle="light-content" backgroundColor={colors.secondary} />
      <SafeAreaView style={{ flex: 0, backgroundColor: colors.secondary }} />

      <View style={{ flex: 1, backgroundColor: colors.secondary }}>
        <KeyboardAvoidingView
          behavior={Platform.OS === "ios" ? "padding" : undefined}
          style={{ flex: 1 }}
        >
          <View style={styles.titleContainer}>
            <Text style={styles.title}>Lion Lift</Text>
            <Text style={styles.subtitle}>PENN STATE ABINGTON</Text>
          </View>

          <View style={styles.sheet}>
            <Text style={styles.heading}>Sign In</Text>

            <CustomTextInput
              label="Penn State Email"
              placeholder="abc123@psu.edu"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
            />

            <CustomTextInput
              label="Password"
              placeholder="Enter your password"
              value={password}
              onChangeText={setPassword}
              isPassword={true}
              onSubmitEditing={handleSignIn}
            />

            <View style={{ flexDirection: "row-reverse" }}>
              <SmallButton
                text="Forgot password?"
                onPress={() =>
                  Alert.alert(
                    "Forgot password",
                    "Password recovery will be added later.",
                  )
                }
              />
            </View>

            <BigButton text="Sign in" onPress={handleSignIn} />

            <Divider />

            <BigButton
              text="Test Backend"
              onPress={testBackend}
              borderOnly={true}
            />

            <Text style={{ textAlign: "center", marginVertical: 12 }}>
              Backend status: {apiLoading ? "Testing..." : apiMessage}
            </Text>

            <BigButton
              text="Create account"
              onPress={() =>
                Alert.alert(
                  "Create account",
                  "Account creation will be added later.",
                )
              }
              borderOnly={true}
            />
          </View>
        </KeyboardAvoidingView>
      </View>
    </Fragment>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    backgroundColor: colors.background,
    margin: 0,
  },
  titleContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: colors.secondary,
    paddingVertical: 24,
  },
  title: {
    color: colors.background,
    fontSize: 40,
    fontWeight: "bold",
    marginBottom: 8,
  },
  subtitle: {
    color: colors.accent,
    fontSize: 16,
    letterSpacing: 2,
  },
  sheet: {
    flex: 4,
    backgroundColor: colors.background,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingHorizontal: 24,
  },
  heading: {
    color: colors.primary,
    fontSize: 32,
    fontWeight: "bold",
    marginVertical: 24,
  },
});