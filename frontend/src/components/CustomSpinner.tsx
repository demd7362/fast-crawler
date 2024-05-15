import {Flex, HStack, Spinner, SpinnerProps, Stack, Text, VStack} from "@chakra-ui/react";

export interface CustomSpinnerProps {
    text: string
}
export default function CustomSpinner({text}:CustomSpinnerProps) {
    return (
        <Flex justify="center" align="center" height="100vh">
            <VStack spacing={6}>
                <Spinner
                    thickness="4px"
                    speed="0.5s"
                    emptyColor="gray.200"
                    color="blue.500"
                    size="xl"
                />
                <Text as={'b'}>{text}</Text>
            </VStack>
        </Flex>
    )
}
