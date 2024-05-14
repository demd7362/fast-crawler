import {Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow} from "@mui/material";
import axios from "axios";
import useSWR from "swr";

interface Post {
    recommendCount: number;
    postUrl: string;
    views: number;
    date: string;
    subject: string;
    writer: string
    writerIp: string;
    title: string;
}

interface Data {

}


export default function View() {
    const {data} = useSWR('http://localhost/api/crawl/github', async () => {
        const response = await axios.get<Post[]>('http://localhost/api/crawl/github');
        console.log(response.data)
        return response.data;
    });


    return (
        <TableContainer component={Paper} className="shadow-lg">
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell className="bg-blue-500 text-white font-bold">말머리</TableCell>
                        <TableCell className="bg-blue-500 text-white font-bold">제목</TableCell>
                        <TableCell className="bg-blue-500 text-white font-bold">글쓴이</TableCell>
                        <TableCell className="bg-blue-500 text-white font-bold">작성일</TableCell>
                        <TableCell className="bg-blue-500 text-white font-bold">조회</TableCell>
                        <TableCell className="bg-blue-500 text-white font-bold">추천</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {data?.map((row:Post, index) => (
                        <TableRow key={row.postUrl} className={index % 2 === 0 ? 'bg-gray-100' : ''}>
                            <TableCell>{row.subject}</TableCell>
                            <TableCell>{row.title}</TableCell>
                            <TableCell>{row.writer}</TableCell>
                            <TableCell>{row.date}</TableCell>
                            <TableCell>{row.views}</TableCell>
                            <TableCell>{row.recommendCount}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
