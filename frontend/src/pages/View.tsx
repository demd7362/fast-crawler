import {
    Box,
    Button,
    Container,
    Flex,
    Icon,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
    VStack
} from "@chakra-ui/react";
import axios from "axios";
import useSWR from "swr";
import CustomSpinner from "../components/CustomSpinner";
import WarningMessage from "../components/WarningMessage";
import {useState} from "react";
import {useParams} from "react-router-dom";
import {FiAward, FiEye, FiThumbsUp} from "react-icons/fi";

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



const endpoint = process.env.REACT_APP_API_URL + "/api/crawl/";
export default function View() {
    const [mode, setMode] = useState<keyof CrawlData>('topLikes');
    const {galleryId} = useParams();
    const requestURI = endpoint + galleryId;
    const { data: crawlResponse, isValidating, error } = useSWR<CrawlResponse>(
        requestURI,
        async () => {
            const response = await axios.get<CrawlResponse>(requestURI);
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
        <Flex justify="center" align="center" height="90vh">
            <VStack spacing={4}>
                <Container maxW="container.xl" px={5}>
                    <Box boxShadow="lg" borderRadius="md" overflow="hidden">
                        <TableContainer>
                            <Table variant="striped" colorScheme="white">
                                <Thead>
                                    <Tr>
                                        <Th bg="blue.500" color="white" fontWeight="bold" py={4}>
                                            순위
                                        </Th>
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
                                    {crawlResponse?.data?.[mode].map((row: Post, index) => (
                                        <Tr key={row.url}>
                                            <Td py={4}>
                                                {index < 3 ? (
                                                    <Icon as={FiAward} color={["gold", "silver", "brown"][index]} />
                                                ) : (
                                                    index + 1
                                                )}
                                            </Td>
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
                                            <Td py={4}>{row.writer}{row.ip ? `(${row.ip})` : ''}</Td>
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
                <Button
                    leftIcon={mode === "topLikes" ? <Icon as={FiThumbsUp} /> : <Icon as={FiEye} />}
                    onClick={() => setMode(mode === "topLikes" ? "topViews" : "topLikes")}
                    colorScheme="blue"
                    size="lg"
                    px={6}
                    py={4}
                    borderRadius="full"
                    boxShadow="md"
                    _hover={{
                        bg: mode === "topLikes" ? "blue.600" : "green.600",
                    }}
                    _active={{
                        bg: mode === "topLikes" ? "blue.700" : "green.700",
                    }}
                >
                    {mode === "topLikes" ? "조회 순으로 보기" : "추천 순으로 보기"}
                </Button>
            </VStack>
        </Flex>
    );
}
