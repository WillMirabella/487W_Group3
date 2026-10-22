import { Children } from "react";
import { StyleSheet, Text, View } from "react-native";
import { rgbaColor } from "react-native-reanimated/lib/typescript/Colors";

type Props = {
  children: string;
  color1?: string;
  color2?: string;
};

export default function GradientText({
  children,
  color1 = "#FF0000",
  color2 = "#00FF00"
}: Props){
  return (
    <View>
        <Text style={styles(Number(children), color1, color2).gradientText}>{children}</Text>
    </View>
  );
}

function getColor(percent: number, color1?: string, color2?: string) {
  const prob = percent / 100;

  const r = Math.round(parseInt(color1?.substring(1, 3) || "0", 16) * (1 - prob) + parseInt(color2?.substring(1, 3) || "0", 16) * prob);
  const g = Math.round(parseInt(color1?.substring(3, 5) || "0", 16) * (1 - prob) + parseInt(color2?.substring(3, 5) || "0", 16) * prob);
  const b = Math.round(parseInt(color1?.substring(5, 7) || "0", 16) * (1 - prob) + parseInt(color2?.substring(5, 7) || "0", 16) * prob);

  return `rgb(${r}, ${g}, ${b})`;
}

const styles = (percent: number, color1?: string, color2?: string) => StyleSheet.create({
  gradientText: {
    color: getColor(percent, color1, color2),
    fontSize: 18,
  },
});
