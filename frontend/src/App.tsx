import './App.css';
import AppRouter from "./router/AppRouter";
import {ChakraProvider, theme} from "@chakra-ui/react";

function App() {
    return (
        <ChakraProvider theme={theme}>
            <AppRouter/>
        </ChakraProvider>
    );
}

export default App;
