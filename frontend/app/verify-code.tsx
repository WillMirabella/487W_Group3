import { Fragment, useState, useEffect } from "react";
import {
  Alert,
  Platform,
  StyleSheet,
  StatusBar,
  Text,
  View,
} from "react-native";
import { colors } from "../constants/colors";
import { KeyboardAvoidingView } from "react-native";
import SmallButton from "../components/buttons/small-button";
import { SafeAreaView } from "react-native-safe-area-context";
import { OtpInput } from "react-native-otp-entry";
import { useLocalSearchParams } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';

export default function SignInScreen() {
  const { email } = useLocalSearchParams();
  const [cooldown, setCooldown] = useState(30);

  function handleResendCode() {
    if (cooldown > 0) return;
    setCooldown(30);
  }

  useEffect(() => {
    if (cooldown === 0) return;

    const timer = setInterval(() => {
      setCooldown((prev) => Math.max(0, prev - 1));
    }, 1000);

    return () => clearInterval(timer);
  }, [cooldown]);

  return (
    <Fragment>
        <StatusBar barStyle="light-content" backgroundColor={colors.secondary} />
        <SafeAreaView style={{ flex: 0, backgroundColor: colors.secondary }} />
        <View style={{ flex: 1, backgroundColor: colors.secondary }}>
          <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined}  style={{ flex: 1 }}>
          <View style={styles.sheet}>
            <Text style={styles.heading}>Enter Code</Text>

            <View style={{gap: '6'}}>
              <Text style={styles.text}>Enter the 6-Digit verfication code sent to: </Text>

              <View style={{flexDirection: 'row', alignItems: 'center', gap: '6'}}>
                <Ionicons name={"mail-outline"} size={24} color={colors.primary} /> 
                <Text style={styles.boldText}>{email}</Text>
              </View>
              
            </View>

            <View style={{ marginTop: 24 }}>
              <OtpInput 
                numberOfDigits={6} 
                onTextChange={(text) => console.log(text)} 
                focusColor={colors.secondary}
                theme={{
                  pinCodeContainerStyle: styles.pinCodeContainer,
                }}
              />
            </View>
            
            <View style={{ flexDirection: "row-reverse" }}>
              <SmallButton
                text={cooldown > 0 ? `Resend Code (${cooldown}s)` : 'Resend Code'}
                disabled={cooldown > 0}
                onPress={() => handleResendCode()}
              ></SmallButton>
            </View>
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
  sheet: {
    flex: 4,
    backgroundColor: colors.background,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingHorizontal: 24,
  },
  subtitle: {
    color: colors.accent,
    fontSize: 16,
    letterSpacing: 2,
  },
  heading: {
    color: colors.primary,
    fontSize: 32,
    fontWeight: "bold",
    marginVertical: 24,
  },
  text: {
    color: colors.primary,
    fontSize: 18,
  },
  boldText: {
    color: colors.primary,
    fontSize: 18,
    fontWeight: "bold",
  },
  pinCodeContainer: {
    borderWidth: 2,
    borderColor: colors.border,
    borderRadius: 16,
    marginVertical: 12,
    backgroundColor: colors.background,
  },
});
