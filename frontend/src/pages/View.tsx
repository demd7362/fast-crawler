import {
    Box,
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Td,
    TableContainer,
    Spinner,
    Container,
    Center,
    AbsoluteCenter, Text, Flex, Icon
} from "@chakra-ui/react";
import axios from "axios";
import useSWR from "swr";
import CustomSpinner from "../components/CustomSpinner";
import {Warning} from "postcss";
import {WarningIcon} from "@chakra-ui/icons";
import WarningMessage from "../components/WarningMessage";
import {useState} from "react";

interface Post {
    recommends: number;
    url: string;
    views: number;
    date: string;
    subject: string;
    writer: string;
    ip: string;
    title: string;
}

interface CrawlData {
    topLikes: Post[];
    topViews: Post[];
}

interface CrawlResponse {
    data?: CrawlData;
    detail: string;
}



const endpoint = "http://localhost/api/crawl/github";
export default function View() {
    const [mode, setMode] = useState()
    const { data: crawlResponse, isValidating, error } = useSWR<CrawlResponse>(
        endpoint,
        async () => {
            const response = await axios.get<CrawlResponse>(endpoint);
            console.log(response.data);
            return response.data;
        }
    );
    if(isValidating){
        return <CustomSpinner text={'데이터를 불러오는 중입니다...'}/>
    }
    if(error){
        return <WarningMessage text={'유효한 갤러리가 아닙니다.'} />
    }
    return (
        <Container maxW="container.xl" px={5}>
            <Box boxShadow="lg" borderRadius="md" overflow="hidden">
                <TableContainer>
                    <Table variant="striped" colorScheme="white">
                        <Thead>
                            <Tr>
                                <Th bg="blue.500" color="white" fontWeight="bold" py={4}>
                                    말머리
                                </Th>
                                <Th bg="blue.500" color="white" fontWeight="bold" py={4}>
                                    제목
                                </Th>
                                <Th bg="blue.500" color="white" fontWeight="bold" py={4}>
                                    글쓴이
                                </Th>
                                <Th bg="blue.500" color="white" fontWeight="bold" py={4}>
                                    작성일
                                </Th>
                                <Th bg="blue.500" color="white" fontWeight="bold" py={4}>
                                    조회
                                </Th>
                                <Th bg="blue.500" color="white" fontWeight="bold" py={4}>
                                    추천
                                </Th>
                            </Tr>
                        </Thead>
                        <Tbody>
                            {crawlResponse?.data?.topViews.map((row: Post, index) => (
                                <Tr key={row.url}>
                                    <Td py={4}>{row.subject}</Td>
                                    <Td py={4}>
                                        <Box
                                            as="a"
                                            href={row.url}
                                            color="blue.500"
                                            fontWeight="semibold"
                                            _hover={{ textDecoration: "underline" }}
                                        >
                                            {row.title}
                                        </Box>
                                    </Td>
                                    <Td py={4}>{row.writer}</Td>
                                    <Td py={4}>{row.date}</Td>
                                    <Td py={4} isNumeric>
                                        {row.views}
                                    </Td>
                                    <Td py={4} isNumeric>
                                        {row.recommends}
                                    </Td>
                                </Tr>
                            ))}
                        </Tbody>
                    </Table>
                </TableContainer>
            </Box>
        </Container>
    );
}
