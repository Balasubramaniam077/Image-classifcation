import React from 'react';
import {
  Text,
  View,
  TouchableOpacity,
  StyleSheet,
  Image,
  Dimensions,
} from 'react-native';

export default function Recommendation({navigation, route}) {
  const {width, height} = Dimensions.get('screen');
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
        Recommendation
      </Text>
      <View style={{alignSelf: 'center', paddingTop: 30, paddingBottom: 50}}>
        <View>
          <Image
            style={{
              width: width / 1.2,
              height: height / 5,
              borderRadius: 10,
            }}
            source={{
              uri: route.params.image.assets[0].uri,
            }}
          />
        </View>
      </View>
      <TouchableOpacity
        onPress={() => {
          navigation.navigate('detail', {detial: route.params.data});
        }}>
        <View
          style={{
            width: '85%',
            alignSelf: 'center',
            borderWidth: 1,
            height: 70,
            borderColor: '#000000',
            borderRadius: 16,
            justifyContent: 'center',
          }}>
          <View style={{paddingLeft: 10}}>
            <Text style={{color: '#000000'}}>{route.params.data.disease}</Text>
          </View>
        </View>
      </TouchableOpacity>
      <View style={{alignSelf: 'center', paddingTop: 50}}>
        <TouchableOpacity
          style={styles.subbutton}
          onPress={() => {
            navigation.navigate('Home');
          }}>
          <Text style={{color: 'white', fontWeight: 'bold', fontSize: 17}}>
            Back
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  subbutton: {
    borderRadius: 10,
    width: 300,
    height: 40,
    backgroundColor: '#34B27B',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
