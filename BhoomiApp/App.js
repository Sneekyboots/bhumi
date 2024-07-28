import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

// Import your screen components
import Dashboard from './screens/Dashboard';
import Market from './screens/Market';
import Insurance from './screens/Insurance';
import FarmManagement from './screens/FarmMangement';
import SupportServices from './screens/SupportServices';
import ProfileSettings from './screens/ProfileSettings';
import Community from './screens/Community';
import CustomDrawerContent from './screens/CustomDrawerContent'; // Import the custom drawer content

const Drawer = createDrawerNavigator();

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <NavigationContainer>
        <Drawer.Navigator
          drawerContent={(props) => <CustomDrawerContent {...props} />}
          screenOptions={{
            drawerStyle: {
              backgroundColor: '#003300', // Light green for plant theme
            },
            drawerActiveTintColor: 'green',
            drawerInactiveTintColor: 'gray',
          }}
        >
          <Drawer.Screen name="Dashboard" component={Dashboard} />
          <Drawer.Screen name="Market" component={Market} />
          <Drawer.Screen name="Insurance" component={Insurance} />
          <Drawer.Screen name="Farm Management" component={FarmManagement} />
          <Drawer.Screen name="Support Services" component={SupportServices} />
          <Drawer.Screen name="Community" component={Community} />
          <Drawer.Screen name="Profile & Settings" component={ProfileSettings} />
        </Drawer.Navigator>
      </NavigationContainer>
    </GestureHandlerRootView>
  );
}
