import Ionicons from '@expo/vector-icons/Ionicons';
import { ScrollView, Text, View } from 'react-native';
import { screenStyles as styles } from '../constants/screen-styles';
import { colors } from '../constants/colors';

type Props = {
  icon: 'car-outline' | 'map-outline' | 'person-outline';
  description: string;
};

export default function PlaceholderScreen({ icon, description }: Props) {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <View style={styles.card}>
        <View accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
          <Ionicons name={icon} size={48} color={colors.primary} />
        </View>
        <Text style={styles.cardTitle}>Coming soon</Text>
        <Text style={styles.description}>{description}</Text>
      </View>
    </ScrollView>
  );
}
