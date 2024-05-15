import {Flex, Icon, Link as ChakraLink, Text, VStack} from "@chakra-ui/react";
import {WarningIcon} from "@chakra-ui/icons";
import {Link, useNavigate} from 'react-router-dom'
import {MouseEventHandler, ReactEventHandler} from "react";

interface WarningMessageProps {
    text: string;
}
export default function WarningMessage({text}: WarningMessageProps) {
    return (
        <Flex justify="center" align="center" height="100vh">
            <VStack spacing={3}>
                <Icon as={WarningIcon} w={12} h={12} color='red.500'/>
                <Text fontSize="3xl" fontWeight="bold">
                    {text}
                </Text>
                <Link to={'/'}>
                    <Text fontWeight={3}>메인으로</Text>
                </Link>
            </VStack>
        </Flex>
    )
}
