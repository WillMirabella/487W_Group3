import Ionicons from '@expo/vector-icons/Ionicons';
import { Tabs } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
      <StatusBar style="dark" />
      <Tabs
        screenOptions={{
          headerTitle: 'LionLift',
          headerTintColor: '#1E407C',
          headerStyle: { backgroundColor: '#FFFFFF' },
          headerShadowVisible: false,
          sceneStyle: { backgroundColor: '#FFFFFF' },
          tabBarActiveTintColor: '#1E407C',
          tabBarInactiveTintColor: '#64748B',
          tabBarActiveBackgroundColor: '#EFF6FF',
          tabBarStyle: { backgroundColor: '#FFFFFF', borderTopColor: '#E2E8F0', minHeight: 64 },
          tabBarLabelPosition: 'below-icon',
          tabBarLabelStyle: { fontSize: 12, fontWeight: '600' },
        }}
      >
        <Tabs.Screen
          name="index"
          options={{
            title: 'Find Drivers',
            tabBarAccessibilityLabel: 'Find Drivers',
            tabBarIcon: ({ color, size }) => (
              <Ionicons name="car-outline" color={color} size={size} />
            ),
          }}
        />
        <Tabs.Screen
          name="map"
          options={{
            title: 'Map',
            tabBarAccessibilityLabel: 'Map',
            tabBarIcon: ({ color, size }) => (
              <Ionicons name="map-outline" color={color} size={size} />
            ),
          }}
        />
        <Tabs.Screen
          name="profile"
          options={{
            title: 'Profile',
            tabBarAccessibilityLabel: 'Profile',
            tabBarIcon: ({ color, size }) => (
              <Ionicons name="person-outline" color={color} size={size} />
            ),
          }}
        />
      </Tabs>
    </>
  );
}
