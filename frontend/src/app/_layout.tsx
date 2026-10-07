import Ionicons from '@expo/vector-icons/Ionicons';
import { Tabs } from 'expo-router';

// NavBar from the UML. Each name matches a screen file in this folder.
export default function NavBar() {
  return (
    <Tabs screenOptions={{
      headerTitle: 'LionLift',
      headerTintColor: '#1E407C',
      headerShadowVisible: false,
      tabBarActiveTintColor: '#1E407C',
      tabBarActiveBackgroundColor: '#EFF6FF',
      tabBarLabelPosition: 'below-icon',
      tabBarStyle: { minHeight: 64 },
    }}>
      <Tabs.Screen name="index" options={{
        title: 'Find Drivers',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="car-outline" color={color} size={size} />
        ),
      }} />
      <Tabs.Screen name="map" options={{
        title: 'Map',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="map-outline" color={color} size={size} />
        ),
      }} />
      <Tabs.Screen name="profile" options={{
        title: 'Profile',
        tabBarIcon: ({ color, size }) => (
          <Ionicons name="person-outline" color={color} size={size} />
        ),
      }} />
    </Tabs>
  );
}
