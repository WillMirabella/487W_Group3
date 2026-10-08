import {
  createStaticNavigation,
} from '@react-navigation/native';
import {
  createBottomTabNavigator,
  createBottomTabScreen,
} from '@react-navigation/bottom-tabs';
import HomeScreen from './components/screens/HomeScreen';
import ProfileScreen from './components/screens/ProfileScreen';
import Ionicons, { IoniconsIconName } from '@react-native-vector-icons/ionicons';

const MyTabs = createBottomTabNavigator({
  screenOptions: ({ route }) => ({
    tabBarIcon: ({ focused, color, size }) => {
      let iconName;

      if (route.name === 'Home') {
        iconName = focused
          ? 'home'
          : 'home-outline';
      } else if (route.name === 'Profile') {
        iconName = focused
          ? 'person'
          : 'person-outline';
      }

      // You can return any component that you like here!
      return <Ionicons name={iconName as IoniconsIconName} size={size} color={color} />;
    },
    tabBarActiveTintColor: 'blue',
    tabBarInactiveTintColor: 'gray',
  }),
  screens: {
    Home: createBottomTabScreen({
      screen: HomeScreen,
      options: {
        tabBarLabel: 'Home',
      },
    }),
    Profile: createBottomTabScreen({
      screen: ProfileScreen,
      options: {
        tabBarLabel: 'Profile',
      },
    }),
  },
});

const Navigation = createStaticNavigation(MyTabs);

export default function App() {
  return <Navigation />;
}