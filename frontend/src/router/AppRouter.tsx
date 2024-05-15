import {BrowserRouter, Route, Routes} from "react-router-dom";
import Main from "../pages/Main";
import View from "../pages/View";
import {SWRConfig} from "swr";

export default function AppRouter() {

    return (
        <SWRConfig
            value={{
                onErrorRetry: (error, key, config, revalidate, { retryCount }) => {
                    if (retryCount > 1) {
                        return;
                    }

                    // 5초 후에 한 번만 재시도
                    setTimeout(() => {
                        revalidate({ retryCount: retryCount + 1 });
                        console.log(`retry count : ${retryCount}`);
                    }, 5000)
                }
            }}
        >
            <BrowserRouter>
                <Routes>
                    <Route path='/' element={<Main/>}/>
                    <Route path='/view' element={<View/>}/>
                </Routes>
            </BrowserRouter>
        </SWRConfig>
    )
}
