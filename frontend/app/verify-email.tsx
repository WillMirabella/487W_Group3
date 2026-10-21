import { Fragment, useState } from "react";
import {
  Alert,
  Platform,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { colors } from "../constants/colors";
import CustomTextInput from "../components/custom-text-input";
import BigButton from "../components/buttons/big-button";
import Divider from "../components/divider";
import { KeyboardAvoidingView } from "react-native";
import Ionicons from '@expo/vector-icons/Ionicons';

export default function SignInScreen() {
  const [email, setEmail] = useState("");
  return (
    <Fragment>
        <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined}  style={{ flex: 1 }}>
          <View style={styles.sheet}>
            <Text style={styles.heading}>Verify PSU Email</Text>

            <View style={styles.bigIcon} accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
              <Ionicons name={"mail-outline"} size={216} color={colors.border} />
            </View>

            <CustomTextInput
              label="Penn State Email"
              placeholder="abc123@psu.edu"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
            />
            <Divider />

            <BigButton
              text="Send Verification Email"
              onPress={() =>
                Alert.alert(
                  "Send Email",
                  "Email verification will be added later.",
                )
              }
              borderOnly={true}
            />
          </View>
        </KeyboardAvoidingView>
    </Fragment>
  );
}

const styles = StyleSheet.create({
  sheet: {
    flex: 4,
    paddingBottom:24,
    justifyContent:"flex-end",
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
    marginTop: 72,
    marginBottom: "auto"
  },
  bigIcon: {
    padding: 0,
    alignItems: 'center',
    justifyContent: "center",
    marginBottom:"auto"
  }
});
