import React from 'react';
import styled from 'styled-components';
import { useUserContext } from '../context/useUserContext';
import { HomePageRecommendations } from './HomePageRecommendations';

const BodyContainer = styled.div`
    padding: 20px 100px;
    margin: 0;
    > div {
        margin-bottom: 20px;
    }
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
`;

export const HomePageBody = () => {
    const user = useUserContext()?.user;
    return <BodyContainer>{user && <HomePageRecommendations user={user} />}</BodyContainer>;
};
