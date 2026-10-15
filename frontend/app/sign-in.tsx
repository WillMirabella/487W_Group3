import { router } from 'expo-router/build/global-state/router';
import React, { useState } from 'react';
import {
  Alert,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  SafeAreaView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

export default function SignInScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  function handleSignIn() {
    // Warning: I have temporatily added an automatic redirect to the Find Drivers tab for demonstration purposes. This will be removed when authentication is implemented.
    router.replace('/(app)/find-drivers');

    // Uncomment the following code when authentication is implemented.
    /*if (!email.trim() || !password) {
      Alert.alert(
        'Missing details',
        'Please enter your email and password.'
      );
      return;
    }

    Alert.alert(
      'Preview only',
      'Authentication will be connected later.'
    );*/
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="#102B5B"
      />

      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <View style={styles.content}>
          <View style={styles.header}>
            

            <Text style={styles.brand}>LionLift</Text>
            <Text style={styles.campus}>PENN STATE ABINGTON</Text>

            <Text style={styles.headline}>
              A Ride for Students.{'\n'}By Students.
            </Text>

            </View>

          <View style={styles.card}>
            <Text style={styles.title}>Welcome back</Text>

            <Text style={styles.description}>
              Sign in or create an account.
            </Text>

            <Text style={styles.label}>Penn State University Email</Text>

            <TextInput
              style={styles.input}
              placeholder="abc123@psu.edu"
              placeholderTextColor="#8592A8"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
              accessibilityLabel="Penn State University Email"
            />

            <Text style={styles.label}>Password</Text>

            <View style={styles.passwordContainer}>
              <TextInput
                style={styles.passwordInput}
                placeholder="Enter your password"
                placeholderTextColor="#8592A8"
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
                autoCapitalize="none"
                autoCorrect={false}
                accessibilityLabel="Password"
                returnKeyType="go"
                onSubmitEditing={handleSignIn}
              />

              <Pressable
                style={styles.showButton}
                onPress={() => setShowPassword(!showPassword)}
                accessibilityRole="button"
                accessibilityLabel={
                  showPassword ? 'Hide password' : 'Show password'
                }
              >
                <Text style={styles.link}>
                  {showPassword ? 'Hide' : 'Show'}
                </Text>
              </Pressable>
            </View>

            <Pressable
              style={styles.forgotButton}
              accessibilityRole="button"
              onPress={() =>
                Alert.alert(
                  'Forgot password',
                  'Password recovery will be added later.'
                )
              }
            >
              <Text style={styles.link}>Forgot password?</Text>
            </Pressable>

            <Pressable
              accessibilityRole="button"
              onPress={handleSignIn}
              style={({ pressed }) => [
                styles.signInButton,
                pressed && styles.buttonPressed,
              ]}
            >
              <Text style={styles.signInText}>Sign in</Text>
            </Pressable>

            <View style={styles.divider} />

            <Text style={styles.accountPrompt}>
              Don’t have an account?
            </Text>

            <Pressable
              accessibilityRole="button"
              onPress={() =>
                Alert.alert(
                  'Create an account',
                  'The account creation screen will be added next.'
                )
              }
              style={({ pressed }) => [
                styles.createButton,
                pressed && styles.createPressed,
              ]}
            >
              <Text style={styles.createText}>
                Create an account
              </Text>
            </Pressable>
          </View>

          <Text style={styles.footer}>
            CONNECTING THE ABINGTON COMMUNITY
          </Text>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  flex: {
    flex: 1,
  },
  container: {
    flex: 1,
    backgroundColor: '#102B5B',
    paddingTop:
      Platform.OS === 'android' ? StatusBar.currentHeight : 0,
  },
  content: {
    flexGrow: 1,
    backgroundColor: '#F1F5FC',
    paddingBottom: 28,
  },
  header: {
    backgroundColor: '#102B5B',
    paddingHorizontal: 30,
    paddingTop: 28,
    paddingBottom: 56,
    alignItems: 'center',
  },
  brand: {
    color: '#FFFFFF',
    fontSize: 28,
    fontWeight: '700',
    marginTop: 10,
  },
  campus: {
    color: '#A9C4FF',
    fontSize: 10,
    letterSpacing: 2,
    marginTop: 8,
  },
  headline: {
    color: '#FFFFFF',
    fontSize: 34,
    fontWeight: '700',
    textAlign: 'center',
    marginTop: 28,
    lineHeight: 41,
  },
  card: {
    backgroundColor: '#FFFFFF',
    width: '90%',
    maxWidth: 440,
    alignSelf: 'center',
    marginTop: -26,
    borderRadius: 24,
    padding: 24,
    shadowColor: '#102B5B',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.1,
    shadowRadius: 16,
    elevation: 5,
  },
  title: {
    color: '#102B5B',
    fontSize: 27,
    fontWeight: '700',
  },
  description: {
    color: '#65738B',
    fontSize: 14,
    marginTop: 8,
    marginBottom: 16,
  },
  label: {
    color: '#293D60',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 9,
  },
  input: {
    borderWidth: 1,
    borderColor: '#DCE4EF',
    borderRadius: 12,
    backgroundColor: '#F9FBFE',
    paddingHorizontal: 15,
    paddingVertical: 11,
    color: '#102B5B',
    fontSize: 16,
    marginBottom: 12,
  },
  passwordContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#DCE4EF',
    borderRadius: 12,
    backgroundColor: '#F9FBFE',
  },
  passwordInput: {
    flex: 1,
    minWidth: 0,
    paddingHorizontal: 15,
    paddingVertical: 11,
    color: '#102B5B',
    fontSize: 16,
  },
  showButton: {
    paddingHorizontal: 15,
    minHeight: 48,
    justifyContent: 'center',
  },
  link: {
    color: '#245BE8',
    fontWeight: '600',
    fontSize: 13,
  },
  forgotButton: {
    alignSelf: 'flex-end',
    paddingVertical: 10,
    marginBottom: 2,
  },
  signInButton: {
    backgroundColor: '#245BE8',
    borderRadius: 12,
    paddingVertical: 13,
    alignItems: 'center',
  },
  buttonPressed: {
    backgroundColor: '#1649C7',
  },
  signInText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
  },
  divider: {
    height: 1,
    backgroundColor: '#E8EDF5',
    marginVertical: 16,
  },
  accountPrompt: {
    color: '#65738B',
    textAlign: 'center',
    fontSize: 14,
    marginBottom: 12,
  },
  createButton: {
    borderWidth: 1,
    borderColor: '#245BE8',
    borderRadius: 12,
    paddingVertical: 13,
    alignItems: 'center',
  },
  createPressed: {
    backgroundColor: '#EDF3FF',
  },
  createText: {
    color: '#245BE8',
    fontSize: 16,
    fontWeight: '700',
  },
  footer: {
    color: '#677A9A',
    fontSize: 9,
    letterSpacing: 1.5,
    textAlign: 'center',
    marginTop: 14,
    paddingHorizontal: 20,
  },
});