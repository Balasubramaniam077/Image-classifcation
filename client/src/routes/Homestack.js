import React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import Home from '../features/Home/';
import Recommendation from '../features/Recommendation';
import Detail_rec from '../features/Detail_Recommendation';

export default function Homestack() {
  const Homestack = createNativeStackNavigator();

  return (
    <Homestack.Navigator
      screenOptions={{animation: 'slide_from_right', headerShown: false}}
      initialRouteName="Home">
      <Homestack.Screen name="Home" component={Home} />
      <Homestack.Screen name="Recommendation" component={Recommendation} />
      <Homestack.Screen name="detail" component={Detail_rec} />
    </Homestack.Navigator>
  );
}
