import {useNavigate} from "react-router-dom";
import {Button, Flex, HStack, Icon, Input, Text, Tooltip, VStack} from "@chakra-ui/react";
import React, {ChangeEvent, useState} from "react";
import {QuestionOutlineIcon} from "@chakra-ui/icons";

export default function Main() {
    const navigate = useNavigate();
    const [galleryId, setGalleryId] = useState<string>('');
    const handleInputChange = (e:ChangeEvent<HTMLInputElement>) => {
        setGalleryId(e.target.value);
    }
    const handleClickSearch = () => {
        if(!galleryId.trim()){
            return;
        }
        navigate(`/view/${galleryId}`);
    }
    const handleKeyUp = (e:React.KeyboardEvent<HTMLInputElement>) => {
        if(e.key === 'Enter'){
            handleClickSearch();
        }
    }
    return (
        <Flex justify="center" align="center" height="100vh">
            <VStack>
                <Tooltip label="https://gall.dcinside.com/board/lists/?id={{ID IS HERE}}" fontSize="xs">
                    <span>
                        <HStack spacing={1}>
                            <Icon as={QuestionOutlineIcon} boxSize={4} color="gray.500" _hover={{color: 'gray.700'}}/>
                            <Text fontWeight={2}>gallery id?</Text>
                        </HStack>
                    </span>
                </Tooltip>
                <HStack spacing={2}>
                    <Input size="lg"
                           onKeyUp={handleKeyUp}
                           onChange={handleInputChange}
                           value={galleryId} variant="filled" placeholder="gallery id 입력" focusBorderColor="purple.500" borderRadius="md" width="400px" _hover={{
                        borderColor: 'purple.500',
                    }} _placeholder={{
                        color: 'gray.500',
                    }} boxShadow="md" mb={4}/>
                    <Button
                        size="lg"
                        mb={4}
                        colorScheme="purple"
                        borderRadius="md"
                        _hover={{
                            bg: 'purple.600',
                        }}
                        _active={{
                            bg: 'purple.700',
                            transform: 'scale(0.98)',
                        }}
                        boxShadow="md"
                        onClick={handleClickSearch}
                    >
                        검색
                    </Button>
                </HStack>
            </VStack>
        </Flex>
    )
}
