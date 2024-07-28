// screens/CustomDrawerContent.js
import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';
import { DrawerContentScrollView, DrawerItemList } from '@react-navigation/drawer';

export default function CustomDrawerContent(props) {
  return (
    <DrawerContentScrollView {...props}>
      <View style={styles.header}>
        {/* Example logo or icon */}
        <Image
          source={require('../assets/dashboard.png')} // Add your logo here
          style={styles.logo}
        />
        <Text style={styles.appName}>Bhumi</Text>
      </View>
      <DrawerItemList {...props} />
    </DrawerContentScrollView>
  );
}

const styles = StyleSheet.create({
  header: {
    backgroundColor: '#e6ffe6',
    padding: 20,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  logo: {
    width: 60,
    height: 60,
    marginBottom: 10,
  },
  appName: {
    fontSize: 24,
    color: '#003300',
    fontWeight: 'bold',
  },
});
