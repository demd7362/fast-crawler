import {BrowserRouter, Route, Routes} from "react-router-dom";
import Main from "../pages/Main";
import View from "../pages/View";
import {SWRConfig} from "swr";

export default function AppRouter() {

    return (
        <SWRConfig
            value={{
                onErrorRetry: (error, key, config, revalidate, { retryCount }) => {
                    console.log(`retry : ${retryCount}`);
                    return; // 아예 재시도 안함


                    // 5초 후에 한 번만 재시도
                    // setTimeout(() => {
                    //     revalidate({ retryCount: retryCount + 1 });
                    //     console.log(`retry count : ${retryCount}`);
                    // }, 5000)
                }
            }}
        >
            <BrowserRouter>
                <Routes>
                    <Route path='/' element={<Main/>}/>
                    <Route path='/view/:galleryId' element={<View/>}/>
                </Routes>
            </BrowserRouter>
        </SWRConfig>
    )
}
