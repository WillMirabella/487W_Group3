import Ionicons from '@expo/vector-icons/Ionicons';
import { Tabs } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

// NavBar from the UML. Each name matches a screen file in this folder.
export default function NavBar() {
  const insets = useSafeAreaInsets();

  return (
    <Tabs initialRouteName="find-drivers" screenOptions={{
      headerTintColor: '#1E407C',
      headerShadowVisible: false,
      tabBarActiveTintColor: '#1E407C',
      tabBarActiveBackgroundColor: '#EFF6FF',
      tabBarLabelPosition: 'below-icon',
      // Use an actual height, including the phone's bottom safe area.
      tabBarStyle: { height: 56 + insets.bottom, backgroundColor: '#FFFFFF' },
    }}>
      <Tabs.Screen name="index" options={{ href: null }} />
      <Tabs.Screen name="find-drivers" options={{
        title: 'Find Drivers',
        tabBarAccessibilityLabel: 'Find Drivers',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="car-outline" color={color} size={size} />
        ),
      }} />
      <Tabs.Screen name="map" options={{
        title: 'Map',
        tabBarAccessibilityLabel: 'Map',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="map-outline" color={color} size={size} />
        ),
      }} />
      <Tabs.Screen name="profile" options={{
        title: 'Profile',
        tabBarAccessibilityLabel: 'Profile',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="person-outline" color={color} size={size} />
        ),
      }} />
      <Tabs.Screen name="sign-in" options={{
        title: 'Sign In',
        tabBarAccessibilityLabel: 'Sign In',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="log-in-outline" color={color} size={size} />
        ),
      }} />
    </Tabs>
  );
}
