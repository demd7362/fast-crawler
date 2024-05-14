import {BrowserRouter, Route, Routes} from "react-router-dom";
import Main from "../pages/Main";
import View from "../pages/View";

export default function AppRouter() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<Main/>}/>
                <Route path='/view' element={<View/>}/>
            </Routes>
        </BrowserRouter>
    )
}
