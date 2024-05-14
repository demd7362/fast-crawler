import {useNavigate} from "react-router-dom";
import axios from "axios";
import useSWR from "swr";


export default function Main() {
    const navigate = useNavigate();
    return (
        <>
            <button onClick={() => {
                navigate('/view');
            }}>view 페이지로
            </button>
            <button onClick={async () => {
                const response = await axios.get('http://localhost/api/crawl/github');
                console.log(response.data);
            }}>api 요청
            </button>
        </>
    )
}
