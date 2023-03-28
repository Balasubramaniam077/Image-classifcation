import {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity} from 'react-native';

function Detail_rec({navigation, route}) {
  const [data, setData] = useState(route.params.detial);
  return (
    <View>
      <Text
        style={{
          textAlign: 'center',
          fontSize: 20,
          color: '#000000',
          fontWeight: 'bold',
          paddingTop: 50,
        }}>
        Detailed Recommendation
      </Text>
      <View style={{padding: 30}}>
        <Text style={styles.topic}>Disease Name</Text>
        <Text style={styles.dis}>{data.disease}</Text>
        <Text style={styles.topic}>Fertilizer</Text>
        <Text style={styles.dis}>{data.fertilizer}</Text>
        <Text style={styles.topic}>Recommendation</Text>
        <Text style={styles.dis}>{data.recommended}</Text>
      </View>
    </View>
  );
}
export default Detail_rec;
const styles = StyleSheet.create({
  topic: {
    fontSize: 23,
    color: '#000000',
  },
  dis: {
    paddingBottom: 20,
    color: '#6e6e6e',
    fontSize: 17,
    paddingTop: 5,
  },
  subbutton: {
    borderRadius: 10,
    width: 300,
    height: 40,
    backgroundColor: '#34B27B',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
